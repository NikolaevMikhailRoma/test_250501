"""
Dependency injection container configuration.
This module sets up the service container for all application dependencies.

This module follows the Dependency Inversion Principle by configuring all
dependencies through abstractions rather than concrete implementations.
"""
from dependency_injector import containers, providers

from backend.domain.interfaces import (
    KnowledgeBaseRepository,
    AIService,
    ContextRetriever,
    QuestionAnswerService,
    HistoryRepository,
    QuestionValidator,
    SourceTracker,
    RelevanceStrategy
)
from backend.domain.ai_interfaces import TextGenerationService, ModelConfigProvider
from data_layer.repositories.csv_repository import CSVKnowledgeBaseRepository
from data_layer.repositories.memory_history_repository import InMemoryHistoryRepository
from data_layer.repositories.relevance_strategies import KeywordMatchingStrategy, TfIdfRelevanceStrategy
from ai_integration.openai_service import OpenAIService
from ai_integration.rag_service import BasicContextRetriever
from backend.services.qa_service import RAGQuestionAnswerService
from backend.services.validators import DefaultQuestionValidator
from backend.services.source_tracker import SimpleSourceTracker


class Container(containers.DeclarativeContainer):
    """
    Dependency injection container for the application.
    
    This container configures and provides all the service dependencies
    required by the application, following the Dependency Inversion Principle.
    It helps with loose coupling between components and makes testing easier.
    """
    
    config = providers.Configuration()
    
    # Configure the relevance strategy
    relevance_strategy = providers.Singleton(
        KeywordMatchingStrategy,
        min_score_threshold=1
    )
    
    # Configure the knowledge base repository
    kb_repository = providers.Singleton(
        CSVKnowledgeBaseRepository,
        csv_path=config.data.csv_path,
        relevance_strategy=relevance_strategy
    )
    
    # Configure the history repository
    history_repository = providers.Singleton(
        InMemoryHistoryRepository,
        max_entries=50
    )
    
    # Configure the question validator
    question_validator = providers.Singleton(
        DefaultQuestionValidator,
        min_length=3
    )
    
    # Configure the source tracker
    source_tracker = providers.Singleton(
        SimpleSourceTracker
    )
    
    # Configure the AI service
    ai_service = providers.Singleton(
        OpenAIService,
        api_key=config.openai.api_key
    )
    
    # Configure the context retriever
    context_retriever = providers.Singleton(
        BasicContextRetriever,
        kb_repository=kb_repository,
        source_tracker=source_tracker
    )
    
    # Configure the QA service
    qa_service = providers.Singleton(
        RAGQuestionAnswerService,
        kb_repository=kb_repository,
        ai_service=ai_service,
        context_retriever=context_retriever,
        question_validator=question_validator,
        source_tracker=source_tracker
    )
