"""
Unit tests for the source tracker.

These tests verify that the source tracker correctly identifies
sources used in generating answers.
"""
import pytest
from backend.services.source_tracker import SimpleSourceTracker, AdvancedSourceTracker


@pytest.fixture
def simple_source_tracker():
    """Create a simple source tracker for testing."""
    return SimpleSourceTracker()


@pytest.fixture
def sample_context():
    """Create a sample context with multiple sources."""
    return """
Source 1:
Question: What is RAG?
Answer: RAG stands for Retrieval-Augmented Generation.

Source 2:
Question: How does RAG work?
Answer: RAG combines retrieval of documents with text generation.

Source 3:
Question: What are the benefits of RAG?
Answer: RAG improves accuracy by grounding responses in factual information.
"""


def test_simple_tracker_explicit_mentions(simple_source_tracker, sample_context):
    """Test tracking sources with explicit mentions."""
    # Arrange
    question = "Tell me about RAG"
    answer = "According to Source 1, RAG stands for Retrieval-Augmented Generation. Source 2 explains that it combines retrieval with generation."
    
    # Act
    sources = simple_source_tracker.track_sources(question, answer, sample_context)
    
    # Assert
    assert "Source 1" in sources
    assert "Source 2" in sources
    assert "Source 3" not in sources


def test_simple_tracker_implicit_mentions(simple_source_tracker, sample_context):
    """Test tracking sources with implicit mentions."""
    # Arrange
    question = "Tell me about RAG"
    answer = "RAG stands for Retrieval-Augmented Generation as mentioned in the first source. The second source tells us it combines retrieval with generation."
    
    # Act
    sources = simple_source_tracker.track_sources(question, answer, sample_context)
    
    # Assert
    assert "Source 1" in sources
    assert "Source 2" in sources


def test_simple_tracker_generic_attribution(simple_source_tracker, sample_context):
    """Test tracking with generic attribution but no specific source."""
    # Arrange
    question = "Tell me about RAG"
    answer = "According to the information provided, RAG stands for Retrieval-Augmented Generation and improves accuracy."
    
    # Act
    sources = simple_source_tracker.track_sources(question, answer, sample_context)
    
    # Assert
    assert len(sources) == 1
    assert "Knowledge Base" in sources


def test_simple_tracker_no_sources(simple_source_tracker):
    """Test tracking when no context is provided."""
    # Arrange
    question = "Tell me about RAG"
    answer = "RAG stands for Retrieval-Augmented Generation."
    
    # Act
    sources = simple_source_tracker.track_sources(question, answer, "")
    
    # Assert
    assert len(sources) == 0
