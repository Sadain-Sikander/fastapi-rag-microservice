"""
Vector store module for ChromaDB integration.
Handles document embedding storage and semantic search operations.
"""

from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings as ChromaSettings
from config import settings


class VectorStore:
    """Manages vector database operations with ChromaDB."""
    
    def __init__(self, collection_name: str = None, persist_dir: str = None):
        """
        Initialize ChromaDB client and collection.
        
        Args:
            collection_name: Name of the ChromaDB collection (default from config)
            persist_dir: Directory for persistent storage (None = in-memory)
        """
        self.collection_name = collection_name or settings.chroma_collection_name
        self.persist_dir = persist_dir or settings.chroma_persist_directory
        
        # Initialize ChromaDB client (in-memory by default)
        # For persistent storage, uncomment the PersistentClient line below
        self.client = chromadb.Client()
        # self.client = chromadb.PersistentClient(path=self.persist_dir)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}  # Use cosine distance for similarity
        )
    
    def add_documents(self, documents: List[str], ids: List[str], metadatas: List[Dict[str, Any]] = None) -> None:
        """
        Add documents to the vector store.
        ChromaDB automatically generates embeddings.
        
        Args:
            documents: List of text chunks to store
            ids: List of unique identifiers for each document
            metadatas: Optional list of metadata dictionaries per document
            
        Raises:
            ValueError: If documents and ids have different lengths
        """
        if len(documents) != len(ids):
            raise ValueError("Number of documents must equal number of ids")
        
        # If no metadata provided, create empty metadata for each doc
        if metadatas is None:
            metadatas = [{} for _ in documents]
        
        try:
            self.collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
        except Exception as e:
            raise ValueError(f"Failed to add documents to vector store: {str(e)}")
    
    def query(self, query_text: str, n_results: int = None) -> Dict[str, Any]:
        """
        Query the vector store for similar documents.
        
        Args:
            query_text: The query text (will be embedded by ChromaDB)
            n_results: Number of results to return (default from config)
            
        Returns:
            Dictionary with 'documents', 'ids', 'distances', and 'metadatas'
        """
        n_results = n_results or settings.top_k_results
        
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            return results
        except Exception as e:
            raise ValueError(f"Failed to query vector store: {str(e)}")
    
    def get_all_documents(self) -> Dict[str, Any]:
        """
        Retrieve all documents from the collection.
        
        Returns:
            Dictionary with 'documents', 'ids', 'distances', and 'metadatas'
        """
        try:
            results = self.collection.get()
            return results
        except Exception as e:
            raise ValueError(f"Failed to retrieve documents: {str(e)}")
    
    def delete_collection(self) -> None:
        """Delete the entire collection and recreate it."""
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            raise ValueError(f"Failed to delete collection: {str(e)}")
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "document_count": count,
                "embedding_model": "default"  # ChromaDB uses its default model
            }
        except Exception as e:
            raise ValueError(f"Failed to get collection stats: {str(e)}")


# Global instance
vector_store = VectorStore()
