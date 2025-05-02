"""
Unit tests for the AI Integration components.
"""
import os
import pytest
from unittest.mock import patch, MagicMock

from backend.domain.interfaces import KnowledgeBaseRepository, FAQEntry
from ai_integration.openai_service import OpenAIService
from ai_integration.rag_service import BasicContextRetriever


class MockKnowledgeBaseRepository(KnowledgeBaseRepository):
    """Mock implementation of KnowledgeBaseRepository for testing."""
    
    def __init__(self, entries=None):
        self.entries = entries or []
    
    def get_relevant_entries(self, question, limit=3):
        """Return mock entries for testing."""
        return self.entries


@pytest.fixture
def mock_entries():
    """Create mock FAQ entries for testing."""
    return [
        FAQEntry(
            id="1",
            question="What is RAG?",
            answer="RAG stands for Retrieval-Augmented Generation."
        ),
        FAQEntry(
            id="2",
            question="How does RAG work?",
            answer="RAG works by retrieving relevant information and augmenting the language model's input."
        )
    ]


@pytest.fixture
def context_retriever(mock_entries):
    """Create a context retriever with mock repository."""
    repo = MockKnowledgeBaseRepository(mock_entries)
    return BasicContextRetriever(repo)


def test_context_retriever_empty():
    """Test context retriever when no entries are found."""
    repo = MockKnowledgeBaseRepository([])
    retriever = BasicContextRetriever(repo)
    
    context = retriever.retrieve("What is AI?")
    
    assert "No relevant information found" in context


def test_context_retriever_with_entries(context_retriever):
    """Test context retriever with mock entries."""
    context = context_retriever.retrieve("What is RAG?")
    
    assert "RAG stands for" in context
    assert "Source 1:" in context
    assert "Source 2:" in context


@patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
def test_openai_service_init():
    """Test OpenAIService initialization with environment variable."""
    service = OpenAIService()
    assert service.api_key == "test_key"


def test_openai_service_init_with_api_key():
    """Test OpenAIService initialization with provided API key."""
    service = OpenAIService(api_key="direct_key")
    assert service.api_key == "direct_key"


def test_openai_service_init_without_api_key():
    """Test OpenAIService initialization fails without API key."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError):
            OpenAIService()


@patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
@patch("openai.OpenAI")
def test_openai_service_generate(mock_openai):
    """Test OpenAIService generate method returns expected response."""
    # Mock the OpenAI client and response
    mock_instance = mock_openai.return_value
    mock_completion = mock_instance.chat.completions.create.return_value
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "This is a mocked response from OpenAI"
    mock_choice.message = mock_message
    mock_completion.choices = [mock_choice]
    
    service = OpenAIService()
    response = service.generate("Test prompt")
    
    # Verify OpenAI was called with the right parameters
    mock_openai.assert_called_once_with(api_key="test_key")
    mock_instance.chat.completions.create.assert_called_once()
    assert "This is a mocked response from OpenAI" == response
