"""
Unit tests for the Question Answer service.

These tests verify that the RAGQuestionAnswerService correctly orchestrates
the question answering process using its dependencies.
"""
import pytest
from unittest.mock import MagicMock, patch

from backend.domain.interfaces import (
    KnowledgeBaseRepository, 
    AIService, 
    ContextRetriever, 
    FAQEntry,
    QuestionValidator,
    SourceTracker
)
from backend.domain.ai_interfaces import TextGenerationService
from backend.domain.exceptions import InvalidQuestionException
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
    # Create a mock that implements both interfaces
    mock = MagicMock()
    # Add the generate method for AIService
    mock.generate = MagicMock(return_value="This is a test answer from AI service.")
    # Add the generate_text method for TextGenerationService
    mock.generate_text = MagicMock(return_value="This is a test answer from AI service.")
    return mock


@pytest.fixture
def mock_context_retriever():
    """Create a mock context retriever."""
    mock = MagicMock(spec=ContextRetriever)
    mock.retrieve.return_value = "Test context about RAG"
    mock.get_sources = MagicMock(return_value=["Source 1"])
    mock.last_context = "Test context about RAG"
    return mock


@pytest.fixture
def mock_question_validator():
    """Create a mock question validator."""
    mock = MagicMock(spec=QuestionValidator)
    mock.validate.return_value = True
    return mock


@pytest.fixture
def mock_source_tracker():
    """Create a mock source tracker."""
    mock = MagicMock(spec=SourceTracker)
    mock.track_sources.return_value = ["Source 1"]
    return mock


@pytest.fixture
def qa_service(mock_kb_repository, mock_ai_service, mock_context_retriever, 
               mock_question_validator, mock_source_tracker):
    """Create a QA service with mock dependencies."""
    return RAGQuestionAnswerService(
        kb_repository=mock_kb_repository,
        ai_service=mock_ai_service,
        context_retriever=mock_context_retriever,
        question_validator=mock_question_validator,
        source_tracker=mock_source_tracker
    )


def test_qa_service_answer(qa_service, mock_context_retriever, mock_ai_service, mock_question_validator):
    """Test the answer method of the QA service."""
    # Act
    result = qa_service.answer("What is RAG?")
    
    # Assert - verify each step was called correctly
    mock_question_validator.validate.assert_called_once_with("What is RAG?")
    mock_context_retriever.retrieve.assert_called_once_with("What is RAG?")
    
    # Check that either generate or generate_text was called
    # Depending on the implementation, one of these should be called
    assert mock_ai_service.generate.call_count + mock_ai_service.generate_text.call_count == 1
    
    assert result == "This is a test answer from AI service."


def test_qa_service_answer_with_sources(qa_service, mock_context_retriever):
    """Test the answer_with_sources method of the QA service."""
    # Act
    answer, sources = qa_service.answer_with_sources("What is RAG?")
    
    # Assert
    assert answer == "This is a test answer from AI service."
    assert sources == ["Source 1"]
    mock_context_retriever.get_sources.assert_called_once()


def test_qa_service_validation_error(qa_service, mock_question_validator):
    """Test that validation errors are properly propagated."""
    # Setup
    mock_question_validator.validate.side_effect = InvalidQuestionException("Too short")
    
    # Act & Assert
    with pytest.raises(InvalidQuestionException):
        qa_service.answer("Hi")


def test_qa_service_create_prompt(qa_service):
    """Test the _create_prompt method of the QA service."""
    # Act
    prompt = qa_service._create_prompt("Test question", "Test context")
    
    # Assert
    assert "Test question" in prompt
    assert "Test context" in prompt
    assert "QUESTION:" in prompt
    assert "AVAILABLE INFORMATION:" in prompt
    assert "mentioning the source number" in prompt  # Check for source reference instructions
