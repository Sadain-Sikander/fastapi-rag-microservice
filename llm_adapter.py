"""
LLM adapter module for multi-provider support.
Abstracts Gemini and Claude APIs with a unified interface.
"""

from typing import Optional, List
from abc import ABC, abstractmethod
import google.generativeai as genai
from anthropic import Anthropic
from config import settings


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """Generate a response from the LLM."""
        pass


class GeminiProvider(LLMProvider):
    """Google Gemini API provider."""
    
    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize Gemini provider.
        
        Args:
            api_key: Google API key (default from config)
            model: Model name (default from config)
        """
        self.api_key = api_key or settings.gemini_api_key
        self.model = model or settings.primary_llm_model
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not configured")
        
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(self.model)
    
    def generate_response(self, prompt: str) -> str:
        """
        Generate response using Gemini API.
        
        Args:
            prompt: The prompt to send to Gemini
            
        Returns:
            Generated text response
            
        Raises:
            Exception: If API call fails
        """
        try:
            response = self.client.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")


class ClaudeProvider(LLMProvider):
    """Anthropic Claude API provider."""
    
    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize Claude provider.
        
        Args:
            api_key: Anthropic API key (default from config)
            model: Model name (default from config)
        """
        self.api_key = api_key or settings.anthropic_api_key
        self.model = model or settings.fallback_llm_model
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not configured")
        
        self.client = Anthropic(api_key=self.api_key)
    
    def generate_response(self, prompt: str) -> str:
        """
        Generate response using Claude API.
        
        Args:
            prompt: The prompt to send to Claude
            
        Returns:
            Generated text response
            
        Raises:
            Exception: If API call fails
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")


class LLMAdapter:
    """Unified adapter for multiple LLM providers with fallback support."""
    
    def __init__(self):
        """Initialize LLM adapter with primary and fallback providers."""
        self.primary_provider = None
        self.fallback_provider = None
        
        # Initialize primary provider (Gemini)
        try:
            if settings.gemini_api_key:
                self.primary_provider = GeminiProvider()
        except Exception as e:
            print(f"Warning: Could not initialize Gemini: {e}")
        
        # Initialize fallback provider (Claude)
        try:
            if settings.anthropic_api_key:
                self.fallback_provider = ClaudeProvider()
        except Exception as e:
            print(f"Warning: Could not initialize Claude: {e}")
        
        if not self.primary_provider and not self.fallback_provider:
            raise RuntimeError("No LLM providers configured. Set GEMINI_API_KEY or ANTHROPIC_API_KEY")
    
    def generate_rag_response(self, question: str, context: List[str]) -> tuple[str, str]:
        """
        Generate a RAG response using context and question.
        
        Args:
            question: User's question
            context: List of relevant context chunks from vector store
            
        Returns:
            Tuple of (response_text, model_used)
            
        Raises:
            RuntimeError: If all providers fail
        """
        # Build the prompt with context
        context_str = "\n\n".join([f"Context {i+1}:\n{chunk}" for i, chunk in enumerate(context)])
        
        prompt = f"""{settings.system_prompt}

Context from documents:
{context_str}

User Question: {question}

Answer based strictly on the context provided above."""
        
        # Try primary provider first
        if self.primary_provider:
            try:
                response = self.primary_provider.generate_response(prompt)
                return response, self.primary_provider.model
            except Exception as e:
                print(f"Primary provider failed: {e}. Falling back to secondary provider.")
        
        # Try fallback provider
        if self.fallback_provider:
            try:
                response = self.fallback_provider.generate_response(prompt)
                return response, self.fallback_provider.model
            except Exception as e:
                print(f"Fallback provider failed: {e}")
                raise RuntimeError(f"All LLM providers failed: {e}")
        
        raise RuntimeError("No working LLM providers available")
    
    def get_active_model(self) -> str:
        """Get the name of the currently active LLM model."""
        if self.primary_provider:
            return self.primary_provider.model
        elif self.fallback_provider:
            return self.fallback_provider.model
        else:
            return "unknown"


# Global instance
llm_adapter = LLMAdapter()
