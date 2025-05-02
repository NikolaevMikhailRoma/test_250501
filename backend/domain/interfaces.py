"""
Core interfaces for the Q&A application following the Dependency Inversion Principle.
All high-level modules should depend on these abstractions.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


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
    
    @abstractmethod
    def answer_with_sources(self, question: str) -> tuple[str, List[str]]:
        """
        Process a question and generate an answer with source information.
        
        Args:
            question: The user's question
            
        Returns:
            Tuple containing (answer, list of sources)
        """
        pass


class HistoryEntry:
    """Data model representing a question-answer history entry."""
    
    def __init__(self, id: str, question: str, answer: str, timestamp: str, sources: Optional[List[str]] = None):
        self.id = id
        self.question = question
        self.answer = answer
        self.timestamp = timestamp
        self.sources = sources or []


class HistoryRepository(ABC):
    """Abstract interface for managing question-answer history."""
    
    @abstractmethod
    def add_entry(self, entry: HistoryEntry) -> None:
        """
        Add a new entry to the history.
        
        Args:
            entry: The history entry to add
        """
        pass
    
    @abstractmethod
    def get_all_entries(self) -> List[HistoryEntry]:
        """
        Retrieve all history entries.
        
        Returns:
            List of all history entries
        """
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all history entries."""
        pass


class QuestionValidator(ABC):
    """Abstract interface for validating questions."""
    
    @abstractmethod
    def validate(self, question: str) -> bool:
        """
        Validate if a question meets the requirements.
        
        Args:
            question: The question to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass


class SourceTracker(ABC):
    """Abstract interface for tracking sources used in answers."""
    
    @abstractmethod
    def track_sources(self, question: str, answer: str, context: str) -> List[str]:
        """
        Track sources used in generating an answer.
        
        Args:
            question: The original question
            answer: The generated answer
            context: The context used to generate the answer
            
        Returns:
            List of source identifiers
        """
        pass


class RelevanceStrategy(ABC):
    """Abstract interface for relevance scoring algorithms."""
    
    @abstractmethod
    def score_relevance(self, question: str, entries: List[FAQEntry], limit: int = 3) -> List[FAQEntry]:
        """
        Score and filter entries based on relevance to the question.
        
        Args:
            question: The user's question
            entries: List of all available entries
            limit: Maximum number of entries to return
            
        Returns:
            List of most relevant entries, limited by the limit parameter
        """
        pass
