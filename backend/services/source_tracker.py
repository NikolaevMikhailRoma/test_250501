"""
Source tracking implementation for the application.
This module provides functionality to track sources used in generating answers.
"""
import re
from typing import List, Set
from backend.domain.interfaces import SourceTracker, FAQEntry


class SimpleSourceTracker(SourceTracker):
    """
    Simple implementation of SourceTracker.
    
    This class provides basic source tracking functionality by
    identifying mentions of source identifiers in the generated answer.
    """
    
    def track_sources(self, question: str, answer: str, context: str) -> List[str]:
        """
        Track sources used in generating an answer.
        
        This implementation extracts source references from the context
        and checks if they are mentioned in the answer.
        
        Args:
            question: The original question
            answer: The generated answer
            context: The context used to generate the answer
            
        Returns:
            List of source identifiers
        """
        # Extract source identifiers from context
        source_pattern = r"Source (\d+):"
        source_ids = re.findall(source_pattern, context)
        
        # Check which sources are mentioned in the answer
        mentioned_sources: Set[str] = set()
        
        for source_id in source_ids:
            # Check if the source is explicitly mentioned
            if f"Source {source_id}" in answer:
                mentioned_sources.add(f"Source {source_id}")
            # Also check for implicit mentions (e.g., "as mentioned in the first source")
            elif source_id == "1" and any(term in answer.lower() for term in ["first source", "source one"]):
                mentioned_sources.add(f"Source {source_id}")
            elif source_id == "2" and any(term in answer.lower() for term in ["second source", "source two"]):
                mentioned_sources.add(f"Source {source_id}")
            elif source_id == "3" and any(term in answer.lower() for term in ["third source", "source three"]):
                mentioned_sources.add(f"Source {source_id}")
        
        # If no specific sources are mentioned but the answer seems to use context
        if not mentioned_sources and any(term in answer.lower() for term in 
                                         ["according to", "as mentioned", "based on", "the information"]):
            # Add a generic source reference
            mentioned_sources.add("Knowledge Base")
        
        return list(mentioned_sources)


class AdvancedSourceTracker(SourceTracker):
    """
    Advanced implementation of SourceTracker.
    
    This class provides more sophisticated source tracking by analyzing
    the semantic similarity between the answer and each source.
    
    In a real implementation, this would use embeddings or other NLP techniques
    to determine which sources influenced the answer.
    """
    
    def track_sources(self, question: str, answer: str, context: str) -> List[str]:
        """
        Track sources used in generating an answer using semantic analysis.
        
        Args:
            question: The original question
            answer: The generated answer
            context: The context used to generate the answer
            
        Returns:
            List of source identifiers
        """
        # For now, use the simple implementation
        # In a real implementation, this would use embeddings or other NLP techniques
        simple_tracker = SimpleSourceTracker()
        return simple_tracker.track_sources(question, answer, context)
