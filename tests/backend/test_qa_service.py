"""
Unit tests for the Question Answer service.
"""
import pytest
from unittest.mock import MagicMock

from backend.domain.interfaces import KnowledgeBaseRepository, AIService, ContextRetriever, FAQEntry
from backend.services.qa_service import RAGQuestionAnswerService


@pytest.fixture
def mock_kb_repository():
    """Create a mock knowledge base repository."""
    mock = MagicMock(spec=KnowledgeBaseRepository)
    mock.get_relevant_entries.return_value = [
        FAQEntry(
            id="1", 
            question="What is RAG?", 
            answer="RAG stands for Retrieval-Augmented Generation."
        )
    ]
    return mock


@pytest.fixture
def mock_ai_service():
    """Create a mock AI service."""
    mock = MagicMock(spec=AIService)
    mock.generate.return_value = "This is a test answer from AI service."
    return mock


@pytest.fixture
def mock_context_retriever():
    """Create a mock context retriever."""
    mock = MagicMock(spec=ContextRetriever)
    mock.retrieve.return_value = "Test context about RAG"
    return mock


@pytest.fixture
def qa_service(mock_kb_repository, mock_ai_service, mock_context_retriever):
    """Create a QA service with mock dependencies."""
    return RAGQuestionAnswerService(
        kb_repository=mock_kb_repository,
        ai_service=mock_ai_service,
        context_retriever=mock_context_retriever
    )


def test_qa_service_answer(qa_service, mock_context_retriever, mock_ai_service):
    """Test the answer method of the QA service."""
    # Act
    result = qa_service.answer("What is RAG?")
    
    # Assert - verify each step was called correctly
    mock_context_retriever.retrieve.assert_called_once_with("What is RAG?")
    mock_ai_service.generate.assert_called_once()
    assert result == "This is a test answer from AI service."


def test_qa_service_create_prompt(qa_service):
    """Test the _create_prompt method of the QA service."""
    # Act
    prompt = qa_service._create_prompt("Test question", "Test context")
    
    # Assert
    assert "Test question" in prompt
    assert "Test context" in prompt
    assert "QUESTION:" in prompt
    assert "AVAILABLE INFORMATION:" in prompt
