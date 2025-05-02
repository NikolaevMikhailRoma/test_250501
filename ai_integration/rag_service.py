"""
Retrieval-Augmented Generation (RAG) implementation.
This module connects the knowledge base and AI components.

This implementation follows the Single Responsibility Principle by separating
context retrieval from source tracking and other concerns.
"""
from typing import List, Optional

from backend.domain.interfaces import ContextRetriever, KnowledgeBaseRepository, FAQEntry, SourceTracker
from backend.services.source_tracker import SimpleSourceTracker


class BasicContextRetriever(ContextRetriever):
    """
    Basic implementation of ContextRetriever that formats relevant entries into a context string.
    
    This class retrieves relevant information from a knowledge base repository based on
    the user's question and formats it into a structured context string that can be
    used by the language model to generate more accurate answers.
    
    The implementation follows the Open/Closed principle allowing for easy extension
    with more sophisticated retrieval methods without modifying existing code.
    """
    
    def __init__(self, kb_repository: KnowledgeBaseRepository, source_tracker: Optional[SourceTracker] = None):
        """
        Initialize the context retriever with a knowledge base repository and optional source tracker.
        
        Args:
            kb_repository: Repository to retrieve knowledge entries from
            source_tracker: Optional tracker for sources used in answers
        """
        self.kb_repository = kb_repository
        self.source_tracker = source_tracker or SimpleSourceTracker()
        self.last_context = ""
        self.last_entries = []
    
    def retrieve(self, question: str) -> str:
        """
        Retrieve and format context for a question based on relevant knowledge base entries.
        
        Args:
            question: The user's question text
            
        Returns:
            A formatted string containing relevant context from the knowledge base
        """
        entries = self.kb_repository.get_relevant_entries(question)
        self.last_entries = entries
        
        if not entries:
            self.last_context = "No relevant information found in the knowledge base."
            return self.last_context
        
        # Format the entries into a context string
        context_parts = []
        for i, entry in enumerate(entries, 1):
            context_parts.append(f"Source {i}:\nQuestion: {entry.question}\nAnswer: {entry.answer}\n")
        
        self.last_context = "\n".join(context_parts)
        return self.last_context
    
    def get_sources(self, answer: str, question: str) -> List[str]:
        """
        Get the sources used in generating an answer.
        
        Args:
            answer: The generated answer
            question: The original question
            
        Returns:
            List of source identifiers
        """
        if not self.last_context or not answer:
            return []
        
        return self.source_tracker.track_sources(question, answer, self.last_context)
