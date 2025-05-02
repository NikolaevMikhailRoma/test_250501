"""
Unit tests for the history repository.

These tests verify that the InMemoryHistoryRepository correctly
stores and retrieves question-answer history.
"""
import pytest
from backend.domain.interfaces import HistoryEntry
from data_layer.repositories.memory_history_repository import InMemoryHistoryRepository


@pytest.fixture
def history_repository():
    """Create a history repository for testing."""
    return InMemoryHistoryRepository(max_entries=3)


@pytest.fixture
def sample_entry():
    """Create a sample history entry for testing."""
    return HistoryEntry(
        id="1",
        question="Test question?",
        answer="Test answer",
        timestamp="2025-05-01T12:00:00",
        sources=["Source 1"]
    )


def test_add_entry(history_repository, sample_entry):
    """Test adding an entry to the repository."""
    # Act
    history_repository.add_entry(sample_entry)
    
    # Assert
    entries = history_repository.get_all_entries()
    assert len(entries) == 1
    assert entries[0].id == sample_entry.id
    assert entries[0].question == sample_entry.question
    assert entries[0].answer == sample_entry.answer


def test_get_all_entries(history_repository, sample_entry):
    """Test retrieving all entries from the repository."""
    # Arrange
    history_repository.add_entry(sample_entry)
    history_repository.add_entry(HistoryEntry(
        id="2",
        question="Another question?",
        answer="Another answer",
        timestamp="2025-05-01T12:30:00"
    ))
    
    # Act
    entries = history_repository.get_all_entries()
    
    # Assert
    assert len(entries) == 2
    assert entries[0].id == "1"
    assert entries[1].id == "2"


def test_clear(history_repository, sample_entry):
    """Test clearing all entries from the repository."""
    # Arrange
    history_repository.add_entry(sample_entry)
    assert len(history_repository.get_all_entries()) == 1
    
    # Act
    history_repository.clear()
    
    # Assert
    assert len(history_repository.get_all_entries()) == 0


def test_max_entries_limit(history_repository):
    """Test that the repository respects the maximum entries limit."""
    # Arrange - add more entries than the limit
    for i in range(5):
        history_repository.add_entry(HistoryEntry(
            id=str(i),
            question=f"Question {i}?",
            answer=f"Answer {i}",
            timestamp=f"2025-05-01T12:{i}0:00"
        ))
    
    # Assert - should only keep the most recent entries
    entries = history_repository.get_all_entries()
    assert len(entries) == 3
    assert entries[0].id == "2"  # Oldest kept
    assert entries[2].id == "4"  # Newest
