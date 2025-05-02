"""
Tests to verify that implementations comply with their interfaces.
This ensures the Liskov Substitution Principle is maintained.
"""
import pytest
from abc import ABC, abstractmethod

from backend.domain.interfaces import (
    KnowledgeBaseRepository,
    AIService,
    ContextRetriever,
    QuestionAnswerService,
    FAQEntry
)
from data_layer.repositories.csv_repository import CSVKnowledgeBaseRepository
from ai_integration.openai_service import OpenAIService
from ai_integration.rag_service import BasicContextRetriever
from backend.services.qa_service import RAGQuestionAnswerService


class TestLiskovSubstitutionPrinciple:
    """Test that implementations properly adhere to their interfaces."""
    
    def test_faq_entry_structure(self):
        """Test the FAQEntry model has the required attributes."""
        entry = FAQEntry(id="1", question="Test?", answer="Answer")
        assert hasattr(entry, "id"), "FAQEntry should have an id attribute"
        assert hasattr(entry, "question"), "FAQEntry should have a question attribute"
        assert hasattr(entry, "answer"), "FAQEntry should have an answer attribute"
        assert entry.id == "1"
        assert entry.question == "Test?"
        assert entry.answer == "Answer"
    
    def test_csv_repository_complies_with_interface(self):
        """Test that CSVKnowledgeBaseRepository implements KnowledgeBaseRepository correctly."""
        # Check inheritance
        assert issubclass(CSVKnowledgeBaseRepository, KnowledgeBaseRepository)
        
        # Check method implementation
        repo = CSVKnowledgeBaseRepository("data/samples/sample_faq.csv")
        
        # Method should accept string and return list of FAQEntry objects
        results = repo.get_relevant_entries("What is RAG?")
        assert isinstance(results, list), "get_relevant_entries should return a list"
        if results:  # If we got results (we should with our sample data)
            assert isinstance(results[0], FAQEntry), "Results should be FAQEntry instances"
    
    def test_openai_service_complies_with_interface(self):
        """Test that OpenAIService implements AIService correctly."""
        # Check inheritance
        assert issubclass(OpenAIService, AIService)
        
        # We can't easily test the actual implementation without mocking OpenAI
        # But we can verify the method exists with the right signature
        assert hasattr(OpenAIService, "generate"), "OpenAIService should implement generate method"
    
    def test_context_retriever_complies_with_interface(self):
        """Test that BasicContextRetriever implements ContextRetriever correctly."""
        # Check inheritance
        assert issubclass(BasicContextRetriever, ContextRetriever)
        
        # Mock a repository
        class MockRepo(KnowledgeBaseRepository):
            def get_relevant_entries(self, question, limit=3):
                return [FAQEntry(id="1", question="Q", answer="A")]
        
        # Create context retriever with mock repo
        retriever = BasicContextRetriever(MockRepo())
        
        # Method should accept string and return string
        result = retriever.retrieve("Test question")
        assert isinstance(result, str), "retrieve should return a string"
    
    def test_qa_service_complies_with_interface(self):
        """Test that RAGQuestionAnswerService implements QuestionAnswerService correctly."""
        # Check inheritance
        assert issubclass(RAGQuestionAnswerService, QuestionAnswerService)
        
        # Method should exist
        assert hasattr(RAGQuestionAnswerService, "answer"), "RAGQuestionAnswerService should implement answer method"
