"""
Main FastAPI application module.
This implements the API endpoints for the Q&A application.

This module follows the Single Responsibility Principle by delegating business logic
to appropriate services and focusing only on API routing and request handling.
"""
import os
import time
import logging
from typing import Optional, List, Dict, Any

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler

from backend.domain.models import QuestionRequest, AnswerResponse, HistoryResponse, HistoryEntry as ApiHistoryEntry
from backend.domain.interfaces import QuestionAnswerService, HistoryRepository, HistoryEntry as DomainHistoryEntry
from backend.domain.exceptions import BaseApplicationException, InvalidQuestionException
from backend.di.containers import Container

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Load environment variables
load_dotenv()

# Setup DI container
container = Container()
container.config.openai.api_key.from_env("OPENAI_API_KEY")
container.config.data.csv_path.from_value(
    os.getenv("FAQ_CSV_PATH", "data/samples/sample_faq.csv")
)

# History is now managed by the HistoryRepository

# Create FastAPI app
app = FastAPI(
    title="AI-Enabled Q&A API",
    description="A Retrieval-Augmented Generation based Question-Answering API",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup dependency injection
@app.on_event("startup")
async def startup():
    """Initialize application services on startup."""
    # Check if API key is available
    if not os.getenv("OPENAI_API_KEY"):
        logging.warning("OPENAI_API_KEY environment variable is not set.")
        logging.warning("The application will fail when calling the OpenAI API.")


def get_qa_service() -> QuestionAnswerService:
    """Dependency provider for QA service."""
    return container.qa_service()


def get_history_repository() -> HistoryRepository:
    """Dependency provider for history repository."""
    return container.history_repository()


# Global exception handler
@app.exception_handler(BaseApplicationException)
async def application_exception_handler(request: Request, exc: BaseApplicationException):
    """Handle application-specific exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


# Define API endpoints
@app.post("/api/ask", response_model=AnswerResponse)
async def ask_question(
    request: QuestionRequest,
    qa_service: QuestionAnswerService = Depends(get_qa_service),
    history_repo: HistoryRepository = Depends(get_history_repository)
):
    """
    Process a question and generate an answer using RAG.
    
    Args:
        request: The question request
        qa_service: Question answering service
        history_repo: Repository for storing question history
        
    Returns:
        Generated answer with sources
    """
    try:
        # The validation is now handled by the QA service
        question = request.question
        
        # Get answer and sources from service
        answer, sources = qa_service.answer_with_sources(question)
        
        # Create history entry
        history_entry = DomainHistoryEntry(
            id=str(int(time.time())),
            question=question,
            answer=answer,
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()),
            sources=sources
        )
        
        # Store in history repository
        history_repo.add_entry(history_entry)
        
        return AnswerResponse(
            answer=answer,
            sources=sources
        )
        
    except InvalidQuestionException as e:
        # Re-raise validation exceptions
        raise e
    except Exception as e:
        # Log the error with proper logging
        logging.error(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process question: {str(e)}")


@app.get("/api/history", response_model=HistoryResponse)
async def get_history(history_repo: HistoryRepository = Depends(get_history_repository)):
    """
    Get the history of questions and answers.
    
    Args:
        history_repo: Repository for accessing question history
    
    Returns:
        History of questions and answers
    """
    # Get entries from repository
    entries = history_repo.get_all_entries()
    
    # Convert domain model to API model
    history_entries = [
        ApiHistoryEntry(
            id=entry.id,
            question=entry.question,
            answer=entry.answer,
            timestamp=entry.timestamp
        ) for entry in entries
    ]
    
    return HistoryResponse(history=history_entries)


@app.get("/health")
def health():
    """Health check endpoint for container monitoring."""
    return {"status": "healthy", "timestamp": int(time.time())}

@app.get("/")
def root():
    """Root endpoint returning API information."""
    return {
        "name": "AI-Enabled Q&A API",
        "version": "0.1.0",
        "description": "A Retrieval-Augmented Generation based Question-Answering API",
        "endpoints": [
            "/api/ask",
            "/api/history",
            "/health",
            "/docs",
            "/redoc",
        ],
    }
