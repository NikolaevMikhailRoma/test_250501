"""
Retrieval-Augmented Generation (RAG) implementation.
This module connects the knowledge base and AI components.
"""
from typing import List

from backend.domain.interfaces import ContextRetriever, KnowledgeBaseRepository, FAQEntry


class BasicContextRetriever(ContextRetriever):
    """
    Basic implementation of ContextRetriever that formats relevant entries into a context string.
    
    This class retrieves relevant information from a knowledge base repository based on
    the user's question and formats it into a structured context string that can be
    used by the language model to generate more accurate answers.
    
    The implementation follows the Open/Closed principle allowing for easy extension
    with more sophisticated retrieval methods without modifying existing code.
    """
    
    def __init__(self, kb_repository: KnowledgeBaseRepository):
        """
        Initialize the context retriever with a knowledge base repository.
        
        Args:
            kb_repository: Repository to retrieve knowledge entries from
        """
        self.kb_repository = kb_repository
    
    def retrieve(self, question: str) -> str:
        """
        Retrieve and format context for a question based on relevant knowledge base entries.
        
        Args:
            question: The user's question text
            
        Returns:
            A formatted string containing relevant context from the knowledge base
        """
        entries = self.kb_repository.get_relevant_entries(question)
        
        if not entries:
            return "No relevant information found in the knowledge base."
        
        # Format the entries into a context string
        context_parts = []
        for i, entry in enumerate(entries, 1):
            context_parts.append(f"Source {i}:\nQuestion: {entry.question}\nAnswer: {entry.answer}\n")
        
        return "\n".join(context_parts)
