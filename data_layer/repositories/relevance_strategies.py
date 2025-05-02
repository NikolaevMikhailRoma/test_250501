"""
Relevance strategy implementations for knowledge base repositories.
This module provides different algorithms for scoring relevance between questions and knowledge base entries.
"""
import re
from typing import List, Dict, Set
from backend.domain.interfaces import RelevanceStrategy, FAQEntry


class KeywordMatchingStrategy(RelevanceStrategy):
    """
    Implementation of RelevanceStrategy using keyword matching.
    
    This strategy extracts keywords from the question and scores entries
    based on how many of these keywords appear in the entry text.
    """
    
    def __init__(self, min_score_threshold: int = 1):
        """
        Initialize the strategy with a minimum score threshold.
        
        Args:
            min_score_threshold: Minimum number of keyword matches required (default: 1)
        """
        self.min_score_threshold = min_score_threshold
        self.stop_words = {
            'a', 'an', 'the', 'and', 'or', 'but', 'is', 'are', 'was', 'were',
            'in', 'on', 'at', 'by', 'for', 'with', 'about', 'to', 'from', 'of',
            'what', 'when', 'where', 'why', 'how', 'which', 'who', 'whom', 'whose'
        }
    
    def score_relevance(self, question: str, entries: List[FAQEntry], limit: int = 3) -> List[FAQEntry]:
        """
        Score and filter entries based on keyword matching relevance to the question.
        
        Args:
            question: The user's question
            entries: List of all available entries
            limit: Maximum number of entries to return
            
        Returns:
            List of most relevant entries, limited by the limit parameter
        """
        # Extract meaningful keywords (exclude common stop words)
        question_keywords = [
            word.lower() for word in re.findall(r'\w+', question.lower()) 
            if word.lower() not in self.stop_words and len(word) > 2
        ]
        
        # If no meaningful keywords found, return empty list
        if not question_keywords:
            return []
            
        scored_entries = []
        
        for entry in entries:
            score = 0
            entry_text = f"{entry.question} {entry.answer}".lower()
            
            for keyword in question_keywords:
                if keyword in entry_text:
                    score += 1
            
            # Only include entries with scores above threshold
            if score >= self.min_score_threshold:
                # Weight entries with more matches higher
                scored_entries.append((score, entry))
        
        # Sort by relevance score (descending) and return top entries
        scored_entries.sort(reverse=True, key=lambda x: x[0])
        return [entry for _, entry in scored_entries[:limit]]


class TfIdfRelevanceStrategy(RelevanceStrategy):
    """
    Implementation of RelevanceStrategy using TF-IDF scoring.
    
    This strategy uses a simplified Term Frequency-Inverse Document Frequency
    approach to score the relevance of entries to a question.
    """
    
    def __init__(self):
        """Initialize the TF-IDF strategy."""
        self.stop_words = {
            'a', 'an', 'the', 'and', 'or', 'but', 'is', 'are', 'was', 'were',
            'in', 'on', 'at', 'by', 'for', 'with', 'about', 'to', 'from', 'of',
            'what', 'when', 'where', 'why', 'how', 'which', 'who', 'whom', 'whose'
        }
    
    def score_relevance(self, question: str, entries: List[FAQEntry], limit: int = 3) -> List[FAQEntry]:
        """
        Score and filter entries based on TF-IDF relevance to the question.
        
        Args:
            question: The user's question
            entries: List of all available entries
            limit: Maximum number of entries to return
            
        Returns:
            List of most relevant entries, limited by the limit parameter
        """
        # Extract question terms
        question_terms = [
            word.lower() for word in re.findall(r'\w+', question.lower()) 
            if word.lower() not in self.stop_words and len(word) > 2
        ]
        
        if not question_terms:
            return []
        
        # Count document frequency for each term
        doc_frequency: Dict[str, int] = {}
        for term in set(question_terms):
            for entry in entries:
                entry_text = f"{entry.question} {entry.answer}".lower()
                if term in entry_text:
                    doc_frequency[term] = doc_frequency.get(term, 0) + 1
        
        # Calculate IDF for each term
        num_docs = len(entries)
        idf: Dict[str, float] = {}
        for term, freq in doc_frequency.items():
            idf[term] = 1.0 + (num_docs / (1.0 + freq))  # Smoothed IDF
        
        # Score each entry
        scored_entries = []
        for entry in entries:
            entry_text = f"{entry.question} {entry.answer}".lower()
            score = 0.0
            
            # Count term frequency in this entry
            term_freq: Dict[str, int] = {}
            for term in question_terms:
                term_freq[term] = entry_text.count(term)
            
            # Calculate TF-IDF score
            for term in question_terms:
                if term in term_freq and term in idf:
                    score += term_freq[term] * idf[term]
            
            if score > 0:
                scored_entries.append((score, entry))
        
        # Sort by score (descending) and return top entries
        scored_entries.sort(reverse=True, key=lambda x: x[0])
        return [entry for _, entry in scored_entries[:limit]]
