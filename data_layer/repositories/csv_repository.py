"""
CSV implementation of the KnowledgeBaseRepository interface.
This module provides functionality to load and query FAQ entries from a CSV file.

This implementation follows the Open/Closed Principle by allowing different
relevance scoring strategies to be injected without modifying the repository code.
"""
import csv
import os
from typing import List, Optional

from backend.domain.interfaces import KnowledgeBaseRepository, FAQEntry, RelevanceStrategy
from data_layer.repositories.relevance_strategies import KeywordMatchingStrategy


class CSVKnowledgeBaseRepository(KnowledgeBaseRepository):
    """
    Implementation of KnowledgeBaseRepository using CSV files as data source.
    
    This class provides access to knowledge base entries stored in CSV format.
    It implements the KnowledgeBaseRepository interface and supports searching
    for relevant entries based on configurable relevance strategies.
    
    The implementation demonstrates both the Liskov Substitution Principle and
    the Open/Closed Principle by fully implementing the base interface contract
    while allowing extension through strategy injection.
    """
    
    def __init__(self, csv_path: str, relevance_strategy: Optional[RelevanceStrategy] = None):
        """
        Initialize repository with path to CSV file and optional relevance strategy.
        
        Args:
            csv_path: Path to the CSV file containing FAQ entries
            relevance_strategy: Strategy to use for scoring relevance (default: KeywordMatchingStrategy)
        """
        self.csv_path = csv_path
        self.entries = []
        self.relevance_strategy = relevance_strategy or KeywordMatchingStrategy()
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
        Uses the configured relevance strategy to score and filter entries.
        
        Args:
            question: The user's question to find relevant entries for
            limit: Maximum number of entries to return (default: 3)
            
        Returns:
            List of FAQEntry objects sorted by relevance to the question
        """
        return self.relevance_strategy.score_relevance(question, self.entries, limit)
