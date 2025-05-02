# AI-Enabled Q&A Web Application

A Retrieval-Augmented Generation (RAG) based Q&A web application that integrates with AI models to provide accurate answers based on a knowledge base. The application follows SOLID principles and clean architecture to ensure maintainability and extensibility.

## Project Structure

This project follows a modular architecture based on SOLID principles:

```
project_root/
├── backend/                     # FastAPI backend service
│   ├── api/                     # REST API endpoints
│   ├── domain/                  # Core business entities and interfaces 
│   │   ├── interfaces.py        # Core domain interfaces
│   │   ├── ai_interfaces.py     # Specialized AI interfaces
│   │   ├── models.py            # API data models
│   │   └── exceptions.py        # Domain-specific exceptions
│   ├── services/                # Business logic implementation
│   │   ├── qa_service.py        # Question answering service
│   │   ├── validators.py        # Validation services
│   │   └── source_tracker.py    # Source tracking services
│   └── di/                      # Dependency injection configuration
│       └── containers.py        # DI container setup
├── ai_integration/              # AI model integration services
│   ├── openai_service.py        # OpenAI implementation
│   └── rag_service.py           # RAG implementation
├── data_layer/                  # Data access and repositories
│   ├── repositories/            # Repository implementations
│   │   ├── csv_repository.py    # CSV knowledge base repository
│   │   ├── memory_history_repository.py # In-memory history repository
│   │   └── relevance_strategies.py # Relevance scoring strategies
│   └── models/                  # Data models
├── frontend/                    # Frontend implementation
└── tests/                       # Unit and integration tests
    └── backend/                 # Backend tests
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 16+ (for frontend)
- OpenAI API key

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Set up Python environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your configuration:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the Application

### Backend

```
uvicorn backend.main:app --reload
```

### Frontend

```
cd frontend
python serve.py
```

Это запустит простой HTTP-сервер на порту 8080 для обслуживания статических файлов фронтенда.

## Docker Deployment

This application can be containerized using Docker for easier deployment and consistency across environments.

### Build and Run with Docker

1. Build the Docker image:
   ```
   docker build -t ai-qa-app .
   ```

2. Run the Docker container:
   ```
   docker run -p 8000:8000 -p 8080:8080 --env-file .env ai-qa-app
   ```
   This exposes both backend (8000) and frontend (8080) ports from the container.

### Using Docker Compose

```
docker-compose up --build
```

## Running Tests

```
pytest
```

### Running Code Quality Audit

```
python tests/code_quality.py
```

## Design Principles

This application strictly follows SOLID principles:

- **Single Responsibility Principle:** Each class has one well-defined responsibility
  - Example: `QuestionAnswerService` orchestrates the QA process, `SourceTracker` tracks sources, `HistoryRepository` manages history
  
- **Open/Closed Principle:** Modules are open for extension but closed for modification
  - Example: `RelevanceStrategy` interface allows adding new relevance algorithms without modifying existing code
  
- **Liskov Substitution Principle:** Implementations are substitutable for their interfaces
  - Example: Different implementations of `KnowledgeBaseRepository` can be swapped without affecting dependent code
  
- **Interface Segregation Principle:** Interfaces are client-specific and focused
  - Example: `AIService` is split into more specific interfaces like `TextGenerationService` and `ModelConfigProvider`
  
- **Dependency Inversion Principle:** High-level modules depend on abstractions
  - Example: All components depend on interfaces rather than concrete implementations, with dependencies injected via the DI container

The RAG (Retrieval-Augmented Generation) architecture enhances AI responses with factual information from the knowledge base, improving accuracy and reliability.
