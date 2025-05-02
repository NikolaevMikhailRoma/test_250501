"""
Integration tests for the entire RAG pipeline.
This tests the interaction between components in a real-world scenario.
"""
import pytest
from unittest.mock import patch, MagicMock

from backend.domain.interfaces import KnowledgeBaseRepository, AIService, FAQEntry
from data_layer.repositories.csv_repository import CSVKnowledgeBaseRepository
from ai_integration.openai_service import OpenAIService
from ai_integration.rag_service import BasicContextRetriever
from backend.services.qa_service import RAGQuestionAnswerService


class TestRAGPipeline:
    """Test the full RAG pipeline integration."""
    
    @pytest.fixture
    def mock_ai_service(self):
        """Create a mock AI service for testing."""
        with patch('openai.OpenAI') as mock_openai:
            # Set up the mock response
            mock_instance = mock_openai.return_value
            mock_completion = mock_instance.chat.completions.create.return_value
            mock_choice = MagicMock()
            mock_message = MagicMock()
            mock_message.content = "This is a mocked answer that includes RAG information."
            mock_choice.message = mock_message
            mock_completion.choices = [mock_choice]
            
            # Create the service with test API key
            service = OpenAIService(api_key="test_api_key")
            yield service
    
    @pytest.fixture
    def sample_csv_path(self):
        """Provide path to the sample FAQ CSV file."""
        return "data/samples/sample_faq.csv"
    
    @pytest.fixture
    def kb_repository(self, sample_csv_path):
        """Create a knowledge base repository using the sample CSV."""
        return CSVKnowledgeBaseRepository(sample_csv_path)
    
    @pytest.fixture
    def context_retriever(self, kb_repository):
        """Create a context retriever with the repository."""
        return BasicContextRetriever(kb_repository)
    
    @pytest.fixture
    def qa_service(self, kb_repository, mock_ai_service, context_retriever):
        """Create the QA service with all dependencies."""
        return RAGQuestionAnswerService(
            kb_repository=kb_repository,
            ai_service=mock_ai_service,
            context_retriever=context_retriever
        )
    
    def test_end_to_end_english_question(self, qa_service, kb_repository):
        """Test the full pipeline with an English question."""
        # First verify that our KB has data
        entries = kb_repository.get_relevant_entries("RAG")
        assert len(entries) > 0, "Knowledge base should have entries about RAG"
        
        # Test the QA service with a question about RAG
        question = "What is RAG and how does it work?"
        answer = qa_service.answer(question)
        
        # Verify the answer is a non-empty string
        assert isinstance(answer, str), "Answer should be a string"
        assert len(answer) > 0, "Answer should not be empty"
        
        # In our mock setup, the answer contains the word RAG
        assert "RAG" in answer, "Answer should contain information about RAG"
    
    def test_end_to_end_russian_question(self, qa_service):
        """Test the full pipeline with a Russian question."""
        # Test the QA service with a Russian question
        question = "Какой размер курицы?"
        answer = qa_service.answer(question)
        
        # Verify the answer is a non-empty string
        assert isinstance(answer, str), "Answer should be a string"
        assert len(answer) > 0, "Answer should not be empty"
    
    def test_prompt_creation(self, qa_service):
        """Test the prompt creation logic in the QA service."""
        prompt = qa_service._create_prompt("Test question", "Test context")
        
        # Verify the prompt contains the question and context
        assert "Test question" in prompt, "Prompt should include the question"
        assert "Test context" in prompt, "Prompt should include the context"
        
        # Check that the prompt follows the expected format
        assert "QUESTION:" in prompt, "Prompt should include a QUESTION section"
        assert "AVAILABLE INFORMATION:" in prompt, "Prompt should include an AVAILABLE INFORMATION section"
