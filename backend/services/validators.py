"""
Validator implementations for the application.
This module provides concrete implementations of validator interfaces.
"""
from backend.domain.interfaces import QuestionValidator
from backend.domain.exceptions import InvalidQuestionException


class DefaultQuestionValidator(QuestionValidator):
    """
    Default implementation of QuestionValidator.
    
    This class provides validation logic for user questions,
    ensuring they meet minimum requirements before processing.
    """
    
    def __init__(self, min_length: int = 3):
        """
        Initialize the validator with minimum requirements.
        
        Args:
            min_length: Minimum length for a valid question (default: 3)
        """
        self.min_length = min_length
    
    def validate(self, question: str) -> bool:
        """
        Validate if a question meets the requirements.
        
        Args:
            question: The question to validate
            
        Returns:
            True if valid, False otherwise
            
        Raises:
            InvalidQuestionException: If the question is invalid
        """
        # Trim whitespace
        question = question.strip()
        
        # Check minimum length
        if len(question) < self.min_length:
            raise InvalidQuestionException(
                f"Question must be at least {self.min_length} characters long."
            )
        
        # Add more validation rules as needed
        
        return True
