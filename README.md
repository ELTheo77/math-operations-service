# Math Operations Microservice

A production-ready microservice for mathematical operations with caching, persistence, and both REST API and CLI interfaces.

## Overview

This microservice provides three mathematical operations:
- **Power**: Calculate base^exponent
- **Fibonacci**: Get the n-th Fibonacci number
- **Factorial**: Calculate n!

### Key Features

- **FastAPI** async framework for high performance
- **Pydantic** models for request/response validation (mandatory requirement)
- **SQLite** database for operation history persistence
- **In-memory caching** with TTL support for improved performance
- **CLI interface** using Click for command-line operations
- **Docker** support for easy deployment
- **Comprehensive logging** and error handling
- **API documentation** with automatic OpenAPI/Swagger UI

## Architecture

The service follows a clean architecture pattern with clear separation of concerns:

```
├── API Layer (FastAPI endpoints)
├── Service Layer (Business logic)
├── Data Layer (SQLAlchemy + SQLite)
└── Cache Layer (In-memory dictionary-based cache)
```

### Design Decisions

1. **Async Architecture**: Used FastAPI with async/await for better performance and scalability
2. **Caching Strategy**: Implemented LRU cache with TTL to balance memory usage and performance
3. **Database Choice**: SQLite for simplicity, easily replaceable with PostgreSQL/MySQL
4. **Error Handling**: Comprehensive error handling with proper HTTP status codes
5. **Extensibility**: Easy to add new operations by extending the OperationType enum

## Installation

### Using Docker (Recommended)

```bash
# Build and run with docker-compose
docker-compose up --build

# Or build manually
docker build -t math-operations .
docker run -p 8000:8000 math-operations
```

### Local Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install CLI
pip install -e .

# Run the service
uvicorn app.main:app --reload
```

## Usage

### REST API

The API is available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`

#### Calculate Power
```bash
curl -X POST "http://localhost:8000/api/v1/calculate" \
  -H "Content-Type: application/json" \
  -d '{"operation": "power", "value": 2, "exponent": 10}'
```

#### Calculate Fibonacci
```bash
curl -X POST "http://localhost:8000/api/v1/calculate" \
  -H "Content-Type: application/json" \
  -d '{"operation": "fibonacci", "value": 10}'
```

#### Calculate Factorial
```bash
curl -X POST "http://localhost:8000/api/v1/calculate" \
  -H "Content-Type: application/json" \
  -d '{"operation": "factorial", "value": 5}'
```

#### View History
```bash
curl "http://localhost:8000/api/v1/history?limit=10"
```

### CLI Interface

After installing the CLI with `pip install -e .`, you can use:

```bash
# Calculate operations
math-cli power --base 2 --exponent 10
math-cli fibonacci --number 20
math-cli factorial --number 5

# View history
math-cli history --limit 10
math-cli history --operation fibonacci

# Cache management
math-cli cache-stats
math-cli clear-cache
```

## Code Quality

The project uses:
- **flake8** for linting (configured in `.flake8`)
- **Type hints** throughout the codebase
- **Pydantic** for data validation
- **Comprehensive error handling**

Run linting:
```bash
flake8 app/ cli/ tests/
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service information |
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/calculate` | Perform calculation |
| GET | `/api/v1/history` | Get operation history |
| GET | `/api/v1/cache/stats` | Cache statistics |
| DELETE | `/api/v1/cache` | Clear cache |

## Configuration

Environment variables (create `.env` file):
```env
DATABASE_URL=sqlite+aiosqlite:///data/math_operations.db
LOG_LEVEL=INFO
CACHE_TTL_SECONDS=3600
CACHE_MAX_SIZE=1000
```

## Performance Considerations

1. **Caching**: Results are cached with LRU eviction and TTL
2. **Async Operations**: All I/O operations are async
3. **Database Indexing**: Operation type is indexed for faster queries
4. **Efficient Algorithms**: 
   - Fibonacci uses dynamic programming
   - Power uses built-in optimized function
   - Factorial uses iterative approach

## Future Enhancements

While keeping within project requirements, potential improvements include:
- Redis for distributed caching
- JWT authentication
- Prometheus metrics integration
- Message queue integration for async processing
- Rate limiting
- GraphQL API option

## Testing

Run tests with:
```bash
pytest tests/ -v
```

## Deployment

The service is containerized and ready for deployment to:
- Kubernetes (add k8s manifests)
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances