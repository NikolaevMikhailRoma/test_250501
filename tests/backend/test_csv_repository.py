"""
Unit tests for the CSV knowledge base repository.
"""
import os
import pytest
from backend.domain.interfaces import FAQEntry
from data_layer.repositories.csv_repository import CSVKnowledgeBaseRepository


@pytest.fixture
def sample_csv_path():
    """Provide the path to sample FAQ CSV."""
    return os.path.join(os.getcwd(), "data", "samples", "sample_faq.csv")


def test_csv_repository_initialization(sample_csv_path):
    """Test that the repository initializes correctly from CSV."""
    repo = CSVKnowledgeBaseRepository(sample_csv_path)
    assert len(repo.entries) > 0
    
    # Check that entries were loaded correctly
    assert all(isinstance(entry, FAQEntry) for entry in repo.entries)
    assert all(hasattr(entry, "id") for entry in repo.entries)
    assert all(hasattr(entry, "question") for entry in repo.entries)
    assert all(hasattr(entry, "answer") for entry in repo.entries)


def test_get_relevant_entries(sample_csv_path):
    """Test retrieving relevant entries for a question."""
    repo = CSVKnowledgeBaseRepository(sample_csv_path)
    
    # Test with a question about RAG
    question = "What is RAG and how does it work?"
    entries = repo.get_relevant_entries(question, limit=2)
    
    # We should get results that match the question keywords
    assert len(entries) > 0
    assert all(isinstance(entry, FAQEntry) for entry in entries)
    
    # The first entry should be about RAG
    assert "RAG" in entries[0].question or "RAG" in entries[0].answer


def test_no_relevant_entries(sample_csv_path):
    """Test behavior when no relevant entries are found."""
    repo = CSVKnowledgeBaseRepository(sample_csv_path)
    
    # Test with a question that shouldn't match anything in the FAQ
    question = "What is the capital of France?"
    entries = repo.get_relevant_entries(question)
    
    # We should get an empty list (not None)
    assert isinstance(entries, list)
    assert len(entries) == 0
