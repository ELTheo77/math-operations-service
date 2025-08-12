# Math Operations Microservice

A production-ready microservice for mathematical operations with caching, persistence, and both REST API and CLI interfaces.

## Overview

This microservice provides three mathematical operations:
- **Power**: Calculate base^exponent
- **Fibonacci**: Get the n-th Fibonacci number
- **Factorial**: Calculate n!

### Key Features

- **FastAPI** async framework for high performance
- **Pydantic** models for request/response validation
- **SQLite** database for operation history persistence
- **Dictionary-based caching** with TTL support
- **CLI interface** using Click for command-line operations
- **Docker** support for easy deployment
- **Comprehensive logging** and error handling
- **Flake8** linting for code quality
- **API documentation** with automatic OpenAPI/Swagger UI

## Project Structure

```
math-operations-service/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py         # API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Settings management
│   │   └── logging.py          # Logging configuration
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py             # Database configuration
│   │   └── session.py          # Session management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py         # SQLAlchemy models
│   │   └── schemas.py          # Pydantic schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── calculator.py       # Math operations logic
│   │   └── cache.py            # Cache service
│   ├── utils/
│   │   └── __init__.py
│   ├── __init__.py
│   └── main.py                 # FastAPI application
├── cli/
│   ├── __init__.py
│   └── commands.py             # Click CLI commands
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_services.py
├── data/                       # SQLite database (created automatically)
├── logs/                       # Application logs (created automatically)
├── .env                        # Environment variables
├── .env.example               # Example environment configuration
├── .flake8                    # Flake8 linting configuration
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt           # Python dependencies
├── run.py                     # Application runner
└── setup.py                   # CLI installation setup
```

## Installation

### Prerequisites
- Python 3.8+ (tested with 3.12)
- pip package manager

### Setup Instructions

1. **Clone the repository and navigate to project directory**
```bash
cd math-operations-service
```

2. **Install dependencies**
```bash
# Install with user flag to avoid permission issues
pip install --user -r requirements.txt

# Or use a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Copy the example file
copy .env.example .env  # Windows
cp .env.example .env  # Linux/Mac
```

4. **Install CLI tool (optional)**
```bash
pip install --user -e .
```

5. **Run the application**
```bash
python run.py
```

The API will be available at `http://localhost:8000`

## Usage

### Running the Application

```bash
python run.py
```

The application requires two terminals:
- **Terminal 1**: Run the API server
- **Terminal 2**: Execute CLI commands or run tests

### REST API Usage

API documentation is available at `http://localhost:8000/docs` when the server is running.

#### Example API Calls

**Power Calculation:**
```bash
curl -X POST "http://localhost:8000/api/v1/calculate" ^
  -H "Content-Type: application/json" ^
  -d "{\"operation\": \"power\", \"value\": 2, \"exponent\": 10}"
```

**Fibonacci Calculation:**
```bash
curl -X POST "http://localhost:8000/api/v1/calculate" ^
  -H "Content-Type: application/json" ^
  -d "{\"operation\": \"fibonacci\", \"value\": 10}"
```

**Factorial Calculation:**
```bash
curl -X POST "http://localhost:8000/api/v1/calculate" ^
  -H "Content-Type: application/json" ^
  -d "{\"operation\": \"factorial\", \"value\": 5}"
```

### CLI Interface Usage

The CLI requires the API to be running. Use a second terminal for CLI commands.

#### Method 1: Python Module (Recommended - Always Works)
```bash
# Navigate to project directory
cd math-operations-service

# Execute commands
python -m cli.commands power --base 2 --exponent 10
python -m cli.commands fibonacci --number 20
python -m cli.commands factorial --number 5
python -m cli.commands history --limit 10
python -m cli.commands cache-stats
python -m cli.commands clear-cache
```

#### Method 2: Using math-cli Command (After pip install -e .)

From Scripts directory (PowerShell):
```bash
cd C:\Users\[YourUsername]\AppData\Roaming\Python\Python312\Scripts
.\math-cli power --base 2 --exponent 10
```

From project directory:
```bash
C:\Users\[YourUsername]\AppData\Roaming\Python\Python312\Scripts\math-cli power --base 2 --exponent 10
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service information |
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/calculate` | Perform calculation |
| GET | `/api/v1/history` | Get operation history |
| GET | `/api/v1/cache/stats` | Cache statistics |
| DELETE | `/api/v1/cache` | Clear cache |

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test files
pytest tests/test_api.py -v
pytest tests/test_services.py -v

# Check code quality
flake8 app/ cli/ tests/
```

## Docker Support

### Using Docker Compose
```bash
# Build and run
docker-compose up --build

# Stop containers
docker-compose down
```

### Manual Docker Build
```bash
# Build image
docker build -t math-operations .

# Run container
docker run -p 8000:8000 math-operations
```

## Configuration

Environment variables in `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `PROJECT_NAME` | Application name | Math Operations Microservice |
| `VERSION` | API version | 1.0.0 |
| `API_V1_STR` | API prefix | /api/v1 |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8000 |
| `DATABASE_URL` | Database connection | sqlite+aiosqlite:///data/math_operations.db |
| `CACHE_TTL_SECONDS` | Cache time-to-live | 3600 |
| `CACHE_MAX_SIZE` | Maximum cache entries | 1000 |
| `LOG_LEVEL` | Logging level | INFO |

## Troubleshooting

### CLI Command Not Found
- Use `python -m cli.commands` instead (works everywhere)
- From Scripts folder use: `.\math-cli` (note the .\ prefix in PowerShell)
- Use full path: `C:\Users\[YourUsername]\AppData\Roaming\Python\Python312\Scripts\math-cli`

### ModuleNotFoundError
- Verify all files are in correct directories (see Project Structure)
- Ensure you're in the project root directory

### Permission Denied During Installation
- Use `pip install --user -r requirements.txt`
- Or use a virtual environment

### Port Already in Use
- Change port in `.env` file
- Or terminate the process using port 8000

### PowerShell Execution
PowerShell requires .\ prefix for executables in current directory:
```powershell
.\math-cli power --base 2 --exponent 10
```

## Project Requirements Compliance

- **Microframework**: FastAPI (async framework)
- **Pydantic**: Used for all request/response serialization
- **Database**: SQLite with SQLAlchemy
- **CLI with Click**: Command-line interface implementation
- **Dictionary-based caching**: In-memory cache with TTL
- **Flake8 linting**: Code quality checks
- **MVC Pattern**: Clean architecture with separation of concerns
- **Extensibility**: Easy to add new operations
- **Production-ready**: Comprehensive error handling and logging