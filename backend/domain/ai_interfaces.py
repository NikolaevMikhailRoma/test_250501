"""
Specialized AI service interfaces following the Interface Segregation Principle.
These interfaces provide more specific contracts for different AI service functionalities.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class TextGenerationService(ABC):
    """
    Interface for text generation services.
    
    This interface follows the Interface Segregation Principle by providing
    a specific contract for text generation with explicit parameters.
    """
    
    @abstractmethod
    def generate_text(
        self,
        prompt: str,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Generate text based on the provided prompt.
        
        Args:
            prompt: The input prompt for the AI model
            model: The model to use for generation
            temperature: Controls randomness (0.0-1.0)
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated text response
        """
        pass


class ModelConfigProvider(ABC):
    """
    Interface for providing model configuration.
    
    This interface follows the Interface Segregation Principle by separating
    configuration concerns from generation functionality.
    """
    
    @abstractmethod
    def get_default_model(self) -> str:
        """
        Get the default model identifier.
        
        Returns:
            Default model identifier
        """
        pass
    
    @abstractmethod
    def get_model_config(self, model_id: str) -> Dict[str, Any]:
        """
        Get configuration for a specific model.
        
        Args:
            model_id: Identifier for the model
            
        Returns:
            Dictionary of model configuration parameters
        """
        pass


class CompletionService(ABC):
    """
    Interface for simple text completion services.
    
    This interface provides a simplified contract for basic text completion
    without the need for complex parameters.
    """
    
    @abstractmethod
    def complete(self, text: str) -> str:
        """
        Complete the given text.
        
        Args:
            text: The text to complete
            
        Returns:
            Completed text
        """
        pass
