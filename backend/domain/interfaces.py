"""
Core interfaces for the Q&A application following the Dependency Inversion Principle.
All high-level modules should depend on these abstractions.
"""
from abc import ABC, abstractmethod
from typing import List, Optional


class FAQEntry:
    """Data model representing a knowledge base entry."""
    
    def __init__(self, id: str, question: str, answer: str):
        self.id = id
        self.question = question
        self.answer = answer


class KnowledgeBaseRepository(ABC):
    """Abstract interface for accessing knowledge base entries."""
    
    @abstractmethod
    def get_relevant_entries(self, question: str, limit: int = 3) -> List[FAQEntry]:
        """
        Retrieve entries from the knowledge base that are relevant to the question.
        
        Args:
            question: The user's question
            limit: Maximum number of entries to return
            
        Returns:
            List of FAQEntry objects relevant to the question
        """
        pass


class AIService(ABC):
    """Abstract interface for generative AI model interactions."""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text based on the provided prompt.
        
        Args:
            prompt: The input prompt for the AI model
            **kwargs: Additional parameters for the AI service
            
        Returns:
            Generated text response
        """
        pass


class ContextRetriever(ABC):
    """Interface for retrieving relevant context from knowledge base."""
    
    @abstractmethod
    def retrieve(self, question: str) -> str:
        """
        Retrieve relevant context for a given question.
        
        Args:
            question: The user's question
            
        Returns:
            String containing the retrieved context
        """
        pass


class QuestionAnswerService(ABC):
    """
    Core service orchestrating the question answering process.
    This interface defines the contract for services that process questions
    and generate answers using various strategies such as RAG.
    """
    
    @abstractmethod
    def answer(self, question: str) -> str:
        """
        Process a question and generate an answer using RAG.
        
        Args:
            question: The user's question
            
        Returns:
            Generated answer based on knowledge base and AI model
        """
        pass
