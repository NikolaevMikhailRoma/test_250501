"""
Dependency injection container configuration.
This module sets up the service container for all application dependencies.
"""
from dependency_injector import containers, providers

from backend.domain.interfaces import (
    KnowledgeBaseRepository,
    AIService,
    ContextRetriever,
    QuestionAnswerService
)
from data_layer.repositories.csv_repository import CSVKnowledgeBaseRepository
from ai_integration.openai_service import OpenAIService
from ai_integration.rag_service import BasicContextRetriever
from backend.services.qa_service import RAGQuestionAnswerService


class Container(containers.DeclarativeContainer):
    """
    Dependency injection container for the application.
    
    This container configures and provides all the service dependencies
    required by the application, following the Dependency Inversion Principle.
    It helps with loose coupling between components and makes testing easier.
    """
    
    config = providers.Configuration()
    
    # Configure the knowledge base repository
    kb_repository = providers.Singleton(
        CSVKnowledgeBaseRepository,
        csv_path=config.data.csv_path
    )
    
    # Configure the AI service
    ai_service = providers.Singleton(
        OpenAIService,
        api_key=config.openai.api_key
    )
    
    # Configure the context retriever
    context_retriever = providers.Singleton(
        BasicContextRetriever,
        kb_repository=kb_repository
    )
    
    # Configure the QA service
    qa_service = providers.Singleton(
        RAGQuestionAnswerService,
        kb_repository=kb_repository,
        ai_service=ai_service,
        context_retriever=context_retriever
    )
