"""
Unit tests for the relevance strategies.

These tests verify that the relevance scoring strategies correctly
identify and rank relevant entries.
"""
import pytest
from backend.domain.interfaces import FAQEntry, RelevanceStrategy
from data_layer.repositories.relevance_strategies import KeywordMatchingStrategy, TfIdfRelevanceStrategy


@pytest.fixture
def sample_entries():
    """Create sample FAQ entries for testing."""
    return [
        FAQEntry(
            id="1",
            question="What is RAG?",
            answer="RAG stands for Retrieval-Augmented Generation."
        ),
        FAQEntry(
            id="2",
            question="How does RAG work?",
            answer="RAG combines retrieval of documents with text generation."
        ),
        FAQEntry(
            id="3",
            question="What are the benefits of AI?",
            answer="AI can automate tasks and provide insights from data."
        ),
        FAQEntry(
            id="4",
            question="What is a language model?",
            answer="A language model is an AI system trained to understand and generate text."
        )
    ]


@pytest.fixture
def keyword_strategy():
    """Create a keyword matching strategy for testing."""
    return KeywordMatchingStrategy(min_score_threshold=1)


@pytest.fixture
def tfidf_strategy():
    """Create a TF-IDF relevance strategy for testing."""
    return TfIdfRelevanceStrategy()


def test_keyword_matching_relevant_entries(keyword_strategy, sample_entries):
    """Test that keyword matching finds relevant entries."""
    # Act
    results = keyword_strategy.score_relevance("Tell me about RAG", sample_entries, limit=2)
    
    # Assert
    assert len(results) == 2
    assert results[0].id == "1" or results[0].id == "2"  # Either of the RAG entries
    assert "RAG" in results[0].question or "RAG" in results[0].answer
    assert "RAG" in results[1].question or "RAG" in results[1].answer


def test_keyword_matching_no_relevant_entries(keyword_strategy, sample_entries):
    """Test that keyword matching returns empty list when no relevant entries."""
    # Act
    results = keyword_strategy.score_relevance("Tell me about blockchain", sample_entries)
    
    # Assert
    assert len(results) == 0


def test_keyword_matching_stop_words(keyword_strategy, sample_entries):
    """Test that keyword matching ignores stop words."""
    # Act
    results = keyword_strategy.score_relevance("What is the RAG and how does it work?", sample_entries)
    
    # Assert
    assert len(results) > 0
    # Should not match on stop words like "what", "is", "the", "and", "how", "does", "it"
    assert all("RAG" in entry.question or "RAG" in entry.answer for entry in results)


def test_tfidf_relevance_strategy(tfidf_strategy, sample_entries):
    """Test that TF-IDF strategy finds relevant entries."""
    # Act
    results = tfidf_strategy.score_relevance("Tell me about language models and AI", sample_entries, limit=2)
    
    # Assert
    assert len(results) > 0
    # Should prioritize entries about language models and AI
    ids = [entry.id for entry in results]
    assert "3" in ids or "4" in ids  # Either the AI benefits or language model entry


def test_tfidf_rare_terms_weight(tfidf_strategy, sample_entries):
    """Test that TF-IDF gives higher weight to rare terms."""
    # Act
    results = tfidf_strategy.score_relevance("language model", sample_entries, limit=2)
    
    # Assert
    assert len(results) > 0
    assert results[0].id == "4"  # The language model entry should be first
