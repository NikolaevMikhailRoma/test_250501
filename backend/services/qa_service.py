"""
Question Answering service implementation.
This module orchestrates the RAG workflow for answering user questions.

This implementation follows the Single Responsibility Principle by focusing solely
on orchestrating the question answering process using injected dependencies.
"""
from typing import List, Optional, Tuple

from backend.domain.interfaces import (
    QuestionAnswerService,
    KnowledgeBaseRepository,
    AIService,
    ContextRetriever,
    SourceTracker,
    QuestionValidator
)
from backend.domain.ai_interfaces import TextGenerationService
from backend.domain.exceptions import InvalidQuestionException


class RAGQuestionAnswerService(QuestionAnswerService):
    """
    Implementation of QuestionAnswerService using Retrieval-Augmented Generation.
    Follows the orchestration pattern, delegating to specialized services.
    
    This implementation demonstrates the Dependency Inversion Principle by depending
    on abstractions rather than concrete implementations.
    """
    
    def __init__(
        self,
        kb_repository: KnowledgeBaseRepository,
        ai_service: TextGenerationService,
        context_retriever: ContextRetriever,
        question_validator: Optional[QuestionValidator] = None,
        source_tracker: Optional[SourceTracker] = None
    ):
        """
        Initialize the QA service with required dependencies.
        
        Args:
            kb_repository: Repository for accessing knowledge base
            ai_service: Service for generating AI responses
            context_retriever: Service for retrieving relevant context
            question_validator: Optional validator for questions
            source_tracker: Optional tracker for sources used in answers
        """
        self.kb_repository = kb_repository
        self.ai_service = ai_service
        self.context_retriever = context_retriever
        self.question_validator = question_validator
        self.source_tracker = source_tracker
    
    def answer(self, question: str) -> str:
        """
        Process a question and generate an answer using RAG.
        
        Args:
            question: The user's question
            
        Returns:
            AI-generated answer incorporating knowledge base information
            
        Raises:
            InvalidQuestionException: If the question is invalid
        """
        # Step 0: Validate the question if a validator is provided
        if self.question_validator:
            self.question_validator.validate(question)
        
        # Step 1: Retrieve relevant context
        context = self.context_retriever.retrieve(question)
        
        # Step 2: Create prompt combining question and context
        prompt = self._create_prompt(question, context)
        
        # Step 3: Generate answer using the AI service
        if isinstance(self.ai_service, TextGenerationService):
            # Use the specialized interface if available
            response = self.ai_service.generate_text(prompt)
        else:
            # Fall back to the general interface
            response = self.ai_service.generate(prompt)
        
        return response
    
    def answer_with_sources(self, question: str) -> Tuple[str, List[str]]:
        """
        Process a question and generate an answer with source information.
        
        Args:
            question: The user's question
            
        Returns:
            Tuple containing (answer, list of sources)
            
        Raises:
            InvalidQuestionException: If the question is invalid
        """
        # Generate the answer
        answer = self.answer(question)
        
        # Track sources if a source tracker is available
        sources = []
        if hasattr(self.context_retriever, 'get_sources'):
            # Use the context retriever's source tracking if available
            sources = self.context_retriever.get_sources(answer, question)
        elif self.source_tracker:
            # Use the dedicated source tracker if available
            context = getattr(self.context_retriever, 'last_context', '')
            sources = self.source_tracker.track_sources(question, answer, context)
        
        return answer, sources
    
    def _create_prompt(self, question: str, context: str) -> str:
        """
        Create a prompt for the AI model that incorporates the question and context.
        
        Args:
            question: The user's question
            context: Retrieved context information
            
        Returns:
            Formatted prompt for the AI model
        """
        return f"""
You are a helpful assistant. Please answer the following question based on the information provided.
If the information doesn't contain the answer, acknowledge that and provide a general response.

QUESTION: {question}

AVAILABLE INFORMATION:
{context}

Your answer should reference the information provided when possible. If you use information from
the available context, make it clear which parts you're referring to by mentioning the source number
(e.g., 'According to Source 1...' or 'As mentioned in Source 2...').

If you're not sure about something, it's okay to say so rather than making up information.
"""
