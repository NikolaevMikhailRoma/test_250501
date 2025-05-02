"""
Main FastAPI application module.
This implements the API endpoints for the Q&A application.
"""
import os
import time
from typing import Optional, List, Dict, Any

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler

from backend.domain.models import QuestionRequest, AnswerResponse, HistoryResponse, HistoryEntry
from backend.domain.interfaces import QuestionAnswerService
from backend.domain.exceptions import BaseApplicationException, InvalidQuestionException
from backend.di.containers import Container

# Load environment variables
load_dotenv()

# Setup DI container
container = Container()
container.config.openai.api_key.from_env("OPENAI_API_KEY")
container.config.data.csv_path.from_value(
    os.getenv("FAQ_CSV_PATH", "data/samples/sample_faq.csv")
)

# Simple in-memory storage for question history
# In a real application, this would be a database
question_history: List[Dict[str, Any]] = []

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
        print("WARNING: OPENAI_API_KEY environment variable is not set.")
        print("The application will fail when calling the OpenAI API.")


def get_qa_service() -> QuestionAnswerService:
    """Dependency provider for QA service."""
    return container.qa_service()


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
    qa_service: QuestionAnswerService = Depends(get_qa_service)
):
    """
    Process a question and generate an answer using RAG.
    
    Args:
        request: The question request
        qa_service: Question answering service
        
    Returns:
        Generated answer
    """
    # Validate the question
    question = request.question.strip()
    if len(question) < 3:
        raise InvalidQuestionException("Question must be at least 3 characters long.")
    
    try:
        # Get answer from service
        answer = qa_service.answer(question)
        
        # Extract sources (implementation would depend on how your QA service returns information)
        # For now, we'll extract FAQ entries that might be mentioned in the answer
        sources = []
        
        # In a real implementation, we would track sources from the QA service
        # Here we're using a simplistic approach for demo purposes
        if "RAG" in answer:
            sources.append("Retrieval-Augmented Generation FAQ")
        
        # Store in history
        history_entry = {
            "id": str(int(time.time())),
            "question": question,
            "answer": answer,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
        }
        question_history.append(history_entry)
        
        # Limit history size
        if len(question_history) > 50:
            question_history.pop(0)  # Remove oldest entry
        
        return AnswerResponse(
            answer=answer,
            sources=sources
        )
        
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process question: {str(e)}")


@app.get("/api/history", response_model=HistoryResponse)
async def get_history():
    """
    Get the history of questions and answers.
    
    Returns:
        History of questions and answers
    """
    history_entries = [HistoryEntry(**entry) for entry in question_history]
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
