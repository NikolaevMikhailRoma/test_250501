"""
CSV implementation of the KnowledgeBaseRepository interface.
This module provides functionality to load and query FAQ entries from a CSV file.
"""
import csv
import os
from typing import List
import re

from backend.domain.interfaces import KnowledgeBaseRepository, FAQEntry


class CSVKnowledgeBaseRepository(KnowledgeBaseRepository):
    """
    Implementation of KnowledgeBaseRepository using CSV files as data source.
    
    This class provides access to knowledge base entries stored in CSV format.
    It implements the KnowledgeBaseRepository interface and supports searching
    for relevant entries based on keyword matching. 
    
    The implementation demonstrates the Liskov Substitution Principle by fully
    implementing the contract defined in the base repository interface while
    adding CSV-specific functionality.
    """
    
    def __init__(self, csv_path: str):
        """
        Initialize repository with path to CSV file.
        
        Args:
            csv_path: Path to the CSV file containing FAQ entries
        """
        self.csv_path = csv_path
        self.entries = []
        self._load_entries()
    
    def _load_entries(self) -> None:
        """Load FAQ entries from CSV file."""
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        
        with open(self.csv_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            self.entries = [
                FAQEntry(
                    id=row.get('id', str(i)),
                    question=row.get('question', ''),
                    answer=row.get('answer', '')
                )
                for i, row in enumerate(reader)
            ]
    
    def get_relevant_entries(self, question: str, limit: int = 3) -> List[FAQEntry]:
        """
        Retrieve entries from CSV that are relevant to the question.
        Uses keyword matching with stop word filtering as the retrieval method.
        
        This method extracts keywords from the user's question, removes common stop words,
        and scores each entry in the knowledge base based on keyword matches. The
        entries with the highest relevance scores are returned.
        
        Args:
            question: The user's question to find relevant entries for
            limit: Maximum number of entries to return (default: 3)
            
        Returns:
            List of FAQEntry objects sorted by relevance to the question
        """
        # Extract meaningful keywords (exclude common stop words)
        stop_words = {
            'a', 'an', 'the', 'and', 'or', 'but', 'is', 'are', 'was', 'were',
            'in', 'on', 'at', 'by', 'for', 'with', 'about', 'to', 'from', 'of',
            'what', 'when', 'where', 'why', 'how', 'which', 'who', 'whom', 'whose'
        }
        question_keywords = [word.lower() for word in re.findall(r'\w+', question.lower()) 
                            if word.lower() not in stop_words and len(word) > 2]
        
        # If no meaningful keywords found, return empty list
        if not question_keywords:
            return []
            
        scored_entries = []
        min_score_threshold = 1  # Require at least this many keyword matches
        
        for entry in self.entries:
            score = 0
            entry_text = f"{entry.question} {entry.answer}".lower()
            
            for keyword in question_keywords:
                if keyword in entry_text:
                    score += 1
            
            # Only include entries with scores above threshold
            if score >= min_score_threshold:
                # Weight entries with more matches higher
                scored_entries.append((score, entry))
        
        # Sort by relevance score (descending) and return top entries
        scored_entries.sort(reverse=True, key=lambda x: x[0])
        return [entry for _, entry in scored_entries[:limit]]
