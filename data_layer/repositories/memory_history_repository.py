"""
In-memory implementation of the HistoryRepository interface.
This module provides functionality to store and retrieve question-answer history in memory.
"""
from typing import List, Optional
from backend.domain.interfaces import HistoryRepository, HistoryEntry


class InMemoryHistoryRepository(HistoryRepository):
    """
    Implementation of HistoryRepository using in-memory storage.
    
    This class provides a simple in-memory storage for question-answer history.
    It implements the HistoryRepository interface and is suitable for
    development or small-scale deployments.
    
    For production use, this would be replaced with a persistent storage solution.
    """
    
    def __init__(self, max_entries: int = 50):
        """
        Initialize the repository with an empty history.
        
        Args:
            max_entries: Maximum number of entries to store (default: 50)
        """
        self.history: List[HistoryEntry] = []
        self.max_entries = max_entries
    
    def add_entry(self, entry: HistoryEntry) -> None:
        """
        Add a new entry to the history.
        
        If the history exceeds the maximum number of entries,
        the oldest entry will be removed.
        
        Args:
            entry: The history entry to add
        """
        self.history.append(entry)
        
        # Limit history size
        if len(self.history) > self.max_entries:
            self.history.pop(0)  # Remove oldest entry
    
    def get_all_entries(self) -> List[HistoryEntry]:
        """
        Retrieve all history entries.
        
        Returns:
            List of all history entries
        """
        return self.history
    
    def clear(self) -> None:
        """Clear all history entries."""
        self.history.clear()
