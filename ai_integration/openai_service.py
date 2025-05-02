"""
OpenAI implementation of the AIService interface.
Handles interaction with OpenAI API for generating responses.
"""
import os
import json
from typing import Dict, Any, Optional

import openai
from backend.domain.interfaces import AIService


class OpenAIService(AIService):
    """
    Implementation of AIService using OpenAI API.
    
    This class handles the integration with OpenAI's language models,
    providing a consistent interface for text generation that follows
    the AIService contract. It manages API key configuration and handles
    the actual API calls to OpenAI's endpoints.
    
    The implementation follows the Single Responsibility Principle by focusing
    solely on OpenAI API interaction and error handling related to this specific service.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OpenAI service.
        
        Args:
            api_key: OpenAI API key. If None, will try to load from environment variable.
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Provide it directly or set OPENAI_API_KEY environment variable.")
        # In production: openai.api_key = self.api_key
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text using OpenAI models.
        
        Args:
            prompt: The input prompt to send to the model
            **kwargs: Additional parameters like model name, temperature, etc.
            
        Returns:
            Generated text response from OpenAI
        """
        model = kwargs.get("model", "gpt-4o")
        temperature = kwargs.get("temperature", 0.7)
        max_tokens = kwargs.get("max_tokens", 1000)
        
        try:
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            # For production, implement proper error handling and logging
            print(f"Error calling OpenAI API: {str(e)}")
            # Fallback to a placeholder response in case of API error
            return f"Error generating response. Please try again later. Details: {str(e)}"
