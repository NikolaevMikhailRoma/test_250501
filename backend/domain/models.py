"""
Pydantic models for the API requests and responses.
"""
from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    """Request model for asking a question."""
    
    question: str = Field(..., min_length=3, description="The user's question")


class AnswerResponse(BaseModel):
    """Response model for question answers."""
    
    answer: str = Field(..., description="The generated answer")
    sources: list[str] = Field(default_factory=list, description="Sources used to generate the answer")


class HistoryEntry(BaseModel):
    """Model for a QA history entry."""
    
    id: str
    question: str
    answer: str
    timestamp: str


class HistoryResponse(BaseModel):
    """Response model for question history.
    
    This model contains a list of history entries representing past questions and answers.
    It is used as the response format for the history API endpoint.
    """
    
    history: list[HistoryEntry] = Field(default_factory=list)
