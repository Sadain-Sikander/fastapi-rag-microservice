"""
Document processing module for PDF extraction and chunking.
Handles PDF file parsing and text segmentation for vector indexing.
"""

import io
from typing import List, Tuple
from pypdf import PdfReader
from config import settings


class DocumentProcessor:
    """Handles PDF extraction and text chunking operations."""
    
    def __init__(self, chunk_size: int = None, overlap: int = 0):
        """
        Initialize the document processor.
        
        Args:
            chunk_size: Size of text chunks (default from config)
            overlap: Number of characters to overlap between chunks (default 0)
        """
        self.chunk_size = chunk_size or settings.chunk_size
        self.overlap = overlap
    
    def extract_text_from_pdf(self, file_content: bytes) -> str:
        """
        Extract all text from a PDF file.
        
        Args:
            file_content: Binary content of the PDF file
            
        Returns:
            Extracted text as a single string
            
        Raises:
            ValueError: If PDF parsing fails
        """
        try:
            pdf_file = io.BytesIO(file_content)
            reader = PdfReader(pdf_file)
            
            text = ""
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- Page {page_num + 1} ---\n{page_text}"
            
            if not text.strip():
                raise ValueError("No text could be extracted from the PDF")
            
            return text
        
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")
    
    def chunk_text(self, text: str, chunk_size: int = None) -> List[str]:
        """
        Split text into fixed-size overlapping chunks.
        
        Args:
            text: Text to chunk
            chunk_size: Size of each chunk (uses instance default if None)
            
        Returns:
            List of text chunks
        """
        chunk_size = chunk_size or self.chunk_size
        chunks = []
        
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end].strip()
            
            if chunk:  # Only add non-empty chunks
                chunks.append(chunk)
            
            # Move start position (with overlap if configured)
            start = end - self.overlap if self.overlap > 0 else end
        
        return chunks
    
    def generate_chunk_ids(self, filename: str, num_chunks: int) -> List[str]:
        """
        Generate deterministic chunk IDs for traceability.
        
        Args:
            filename: Name of the source PDF file
            num_chunks: Number of chunks
            
        Returns:
            List of unique chunk IDs
        """
        # Remove .pdf extension if present
        clean_filename = filename.replace(".pdf", "").replace(" ", "_")
        
        return [f"doc_{clean_filename}_chunk_{i}" for i in range(num_chunks)]
    
    def process_document(self, file_content: bytes, filename: str) -> Tuple[List[str], List[str]]:
        """
        Complete pipeline: extract text, chunk, and generate IDs.
        
        Args:
            file_content: Binary PDF content
            filename: Original filename for ID generation
            
        Returns:
            Tuple of (chunks, chunk_ids)
            
        Raises:
            ValueError: If processing fails at any step
        """
        # Extract text from PDF
        text = self.extract_text_from_pdf(file_content)
        
        # Split into chunks
        chunks = self.chunk_text(text)
        
        # Generate IDs
        chunk_ids = self.generate_chunk_ids(filename, len(chunks))
        
        return chunks, chunk_ids


# Global instance
document_processor = DocumentProcessor()
