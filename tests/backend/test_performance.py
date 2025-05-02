"""
Performance benchmarks for critical components.
These tests help identify performance bottlenecks in the system.
"""
import time
import pytest
from unittest.mock import patch, MagicMock

from data_layer.repositories.csv_repository import CSVKnowledgeBaseRepository
from ai_integration.rag_service import BasicContextRetriever


class TestPerformanceBenchmarks:
    """Performance tests for key components."""
    
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
    
    def test_repository_performance(self, kb_repository):
        """Benchmark the repository's query performance."""
        # Prepare test data
        test_queries = [
            "What is RAG?",
            "How does retrieval work?",
            "Can you explain knowledge bases?",
            "Tell me about fine-tuning versus RAG",
            "What challenges exist in RAG systems?"
        ]
        
        # Measure the time taken for multiple queries
        total_time = 0
        for query in test_queries:
            start_time = time.time()
            results = kb_repository.get_relevant_entries(query)
            elapsed = time.time() - start_time
            total_time += elapsed
            
            # Basic assertions
            assert isinstance(results, list), "Results should be a list"
            # Queries should return results in reasonable time
            assert elapsed < 0.5, f"Query '{query}' took too long: {elapsed:.4f}s"
        
        # Calculate and report average time
        avg_time = total_time / len(test_queries)
        print(f"Average repository query time: {avg_time:.4f}s")
        
        # Time should be reasonable for a small dataset
        assert avg_time < 0.1, f"Average query time too high: {avg_time:.4f}s"
    
    def test_context_retriever_performance(self, context_retriever):
        """Benchmark the context retriever's performance."""
        # Prepare test data
        test_queries = [
            "What is RAG?",
            "How does retrieval work?", 
            "Tell me about knowledge bases",
            "What are the challenges of RAG?"
        ]
        
        # Measure time for context retrieval
        total_time = 0
        for query in test_queries:
            start_time = time.time()
            context = context_retriever.retrieve(query)
            elapsed = time.time() - start_time
            total_time += elapsed
            
            # Basic assertions
            assert isinstance(context, str), "Context should be a string"
            assert len(context) > 0, "Context should not be empty"
        
        # Calculate and report average time
        avg_time = total_time / len(test_queries)
        print(f"Average context retrieval time: {avg_time:.4f}s")
        
        # Time should be reasonable
        assert avg_time < 0.2, f"Average context retrieval time too high: {avg_time:.4f}s"
    
    def test_repository_scaling(self, sample_csv_path):
        """Test how the repository handles repeated initializations (e.g., in serverless environments)."""
        # Measure time to initialize repository multiple times
        init_times = []
        
        for _ in range(5):  # Simulate multiple initializations
            start_time = time.time()
            repo = CSVKnowledgeBaseRepository(sample_csv_path)
            init_time = time.time() - start_time
            init_times.append(init_time)
            
            # Basic verification
            assert len(repo.entries) > 0, "Repository should load entries"
        
        # Calculate and report statistics
        avg_init_time = sum(init_times) / len(init_times)
        max_init_time = max(init_times)
        
        print(f"Average repository initialization time: {avg_init_time:.4f}s")
        print(f"Maximum repository initialization time: {max_init_time:.4f}s")
        
        # Times should be reasonable
        assert avg_init_time < 0.1, f"Average initialization time too high: {avg_init_time:.4f}s"
        assert max_init_time < 0.2, f"Maximum initialization time too high: {max_init_time:.4f}s"
