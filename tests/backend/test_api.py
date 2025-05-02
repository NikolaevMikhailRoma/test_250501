"""
Integration tests for the FastAPI endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from backend.main import app, container
from backend.domain.interfaces import QuestionAnswerService


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def mock_qa_service():
    """Create a mock QA service."""
    # Создаем мок без spec, чтобы можно было добавлять методы
    mock = MagicMock()
    # Затем добавляем методы, которые нам нужны
    mock.answer = MagicMock(return_value="This is a mock answer for testing.")
    mock.answer_with_sources = MagicMock(return_value=("This is a mock answer for testing.", ["Source 1"]))
    return mock


@pytest.fixture
def test_client(mock_qa_service):
    """Create a test client with mocked services."""
    # Patch the container's qa_service directly
    original_qa_service = container.qa_service
    container.qa_service = lambda: mock_qa_service
    
    client = TestClient(app)
    
    yield client
    
    # Restore the original service after the test
    container.qa_service = original_qa_service


def test_ask_question_success(test_client, mock_qa_service):
    """Test the ask question endpoint with a valid question."""
    # Arrange
    mock_qa_service.answer_with_sources.return_value = ("This is an answer about RAG systems.", ["Source 1"])
    
    # Act
    response = test_client.post("/api/ask", json={"question": "What is RAG?"})
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "This is an answer about RAG systems."
    assert "sources" in data
    assert data["sources"] == ["Source 1"]
    mock_qa_service.answer_with_sources.assert_called_once_with("What is RAG?")


def test_ask_question_invalid_request(test_client):
    """Test the ask question endpoint with an invalid request."""
    # Empty question
    response = test_client.post("/api/ask", json={"question": ""})
    assert response.status_code == 422
    
    # Missing question field
    response = test_client.post("/api/ask", json={})
    assert response.status_code == 422


def test_ask_question_service_error(test_client, mock_qa_service):
    """Test the ask question endpoint when service raises an exception."""
    # Arrange
    mock_qa_service.answer_with_sources.side_effect = Exception("Service error")
    
    # Act
    response = test_client.post("/api/ask", json={"question": "What is RAG?"})
    
    # Assert
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
    assert "Failed to process question" in data["detail"]


def test_get_history(test_client):
    """Test the history endpoint."""
    # Act
    response = test_client.get("/api/history")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "history" in data
    assert isinstance(data["history"], list)
