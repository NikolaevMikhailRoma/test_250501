"""
Custom exceptions for the application.
This module defines application-specific exceptions that can be handled appropriately.
"""
from typing import Optional


class BaseApplicationException(Exception):
    """
    Base exception class for application-specific exceptions.
    
    This is the foundation class for all custom exceptions in the application.
    It includes support for HTTP status codes for proper API error responses.
    """
    
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class RepositoryException(BaseApplicationException):
    """Exception raised for errors in the data repository."""
    
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message, status_code)


class AIServiceException(BaseApplicationException):
    """Exception raised for errors in AI service integration."""
    
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message, status_code)


class InvalidQuestionException(BaseApplicationException):
    """
    Exception raised when a question is invalid or cannot be processed.
    
    This is typically raised when a question is too short, empty,
    or otherwise does not meet the requirements for processing.
    Returns a 400 Bad Request status code.
    """
    
    def __init__(self, message: str = "The question cannot be processed."):
        """
        Initialize the exception with a custom message and 400 status code.
        
        Args:
            message: Custom error message (default: 'The question cannot be processed.')
        """
        super().__init__(message, status_code=400)
