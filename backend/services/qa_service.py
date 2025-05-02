"""
Question Answering service implementation.
This module orchestrates the RAG workflow for answering user questions.
"""
from backend.domain.interfaces import (
    QuestionAnswerService,
    KnowledgeBaseRepository,
    AIService,
    ContextRetriever
)


class RAGQuestionAnswerService(QuestionAnswerService):
    """
    Implementation of QuestionAnswerService using Retrieval-Augmented Generation.
    Follows the orchestration pattern, delegating to specialized services.
    """
    
    def __init__(
        self,
        kb_repository: KnowledgeBaseRepository,
        ai_service: AIService,
        context_retriever: ContextRetriever
    ):
        """
        Initialize the QA service with required dependencies.
        
        Args:
            kb_repository: Repository for accessing knowledge base
            ai_service: Service for generating AI responses
            context_retriever: Service for retrieving relevant context
        """
        self.kb_repository = kb_repository
        self.ai_service = ai_service
        self.context_retriever = context_retriever
    
    def answer(self, question: str) -> str:
        """
        Process a question and generate an answer using RAG.
        
        Args:
            question: The user's question
            
        Returns:
            AI-generated answer incorporating knowledge base information
        """
        # Step 1: Retrieve relevant context
        context = self.context_retriever.retrieve(question)
        
        # Step 2: Create prompt combining question and context
        prompt = self._create_prompt(question, context)
        
        # Step 3: Generate answer using the AI service
        response = self.ai_service.generate(prompt)
        
        return response
    
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
the available context, make it clear which parts you're referring to.
"""
