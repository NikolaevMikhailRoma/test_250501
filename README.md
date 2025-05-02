# AI-Enabled Q&A Web Application

A Retrieval-Augmented Generation (RAG) based Q&A web application that integrates with AI models to provide accurate answers based on a knowledge base.

## Project Structure

This project follows a modular architecture based on SOLID principles:

```
project_root/
├── backend/              # FastAPI backend service
│   ├── api/              # REST API endpoints
│   ├── domain/           # Core business entities and interfaces 
│   ├── services/         # Business logic implementation
│   ├── infrastructure/   # External service integrations
│   └── di/               # Dependency injection configuration
├── ai_integration/       # AI model integration services
├── data_layer/           # Data access and repositories
│   ├── repositories/     # Repository implementations
│   └── models/           # Data models
├── frontend/             # React/Vue/Angular frontend
└── tests/                # Unit and integration tests
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

This application follows SOLID principles:

- **Single Responsibility:** Each class has one responsibility
- **Open/Closed:** Modules are open for extension but closed for modification
- **Liskov Substitution:** Implementations are substitutable for their interfaces
- **Interface Segregation:** Interfaces are client-specific
- **Dependency Inversion:** High-level modules depend on abstractions

The RAG (Retrieval-Augmented Generation) architecture enhances AI responses with factual information from the knowledge base.
