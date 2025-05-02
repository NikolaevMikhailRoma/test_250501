"""
OpenAI implementation of the specialized AI service interfaces.
Handles interaction with OpenAI API for generating responses.

This implementation follows the Interface Segregation Principle by implementing
specialized interfaces rather than a single general-purpose interface.
"""
import os
import json
import logging
from typing import Dict, Any, Optional

import openai
from backend.domain.interfaces import AIService
from backend.domain.ai_interfaces import TextGenerationService, ModelConfigProvider


class OpenAIService(AIService, TextGenerationService, ModelConfigProvider):
    """
    Implementation of AI service interfaces using OpenAI API.
    
    This class handles the integration with OpenAI's language models,
    providing specialized interfaces for different aspects of AI functionality.
    It manages API key configuration and handles API calls to OpenAI's endpoints.
    
    The implementation follows both the Single Responsibility Principle and
    the Interface Segregation Principle by providing focused interfaces
    for specific aspects of AI functionality.
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
        Generate text using OpenAI models (legacy method).
        
        This method is maintained for backward compatibility with the AIService interface.
        New code should use the more specific generate_text method instead.
        
        Args:
            prompt: The input prompt to send to the model
            **kwargs: Additional parameters like model name, temperature, etc.
            
        Returns:
            Generated text response from OpenAI
        """
        return self.generate_text(
            prompt=prompt,
            model=kwargs.get("model", "gpt-4o"),
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 1000)
        )
    
    def generate_text(self, prompt: str, model: str = "gpt-4o", temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """
        Generate text using OpenAI models with explicit parameters.
        
        Args:
            prompt: The input prompt to send to the model
            model: The model to use for generation
            temperature: Controls randomness (0.0-1.0)
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated text response from OpenAI
        """
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
            # Use proper logging instead of print
            logging.error(f"Error calling OpenAI API: {str(e)}")
            # Fallback to a placeholder response in case of API error
            return f"Error generating response. Please try again later. Details: {str(e)}"
    
    def get_default_model(self) -> str:
        """
        Get the default model identifier.
        
        Returns:
            Default model identifier
        """
        return "gpt-4o"
    
    def get_model_config(self, model_id: str) -> Dict[str, Any]:
        """
        Get configuration for a specific model.
        
        Args:
            model_id: Identifier for the model
            
        Returns:
            Dictionary of model configuration parameters
        """
        # Default configurations for different models
        configs = {
            "gpt-4o": {
                "temperature": 0.7,
                "max_tokens": 1000,
                "top_p": 1.0
            },
            "gpt-3.5-turbo": {
                "temperature": 0.7,
                "max_tokens": 1000,
                "top_p": 1.0
            }
        }
        
        # Return the config for the requested model, or a default if not found
        return configs.get(model_id, {
            "temperature": 0.7,
            "max_tokens": 1000,
            "top_p": 1.0
        })
