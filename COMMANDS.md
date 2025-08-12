# Commands Reference

## Starting the Application

### Terminal 1 - API Server
```bash
python run.py
```
Keep this terminal running. API is available at http://localhost:8000

## CLI Commands (Terminal 2)

### Method 1: Python Module (Recommended)
```bash
# Navigate to project directory
cd math-operations-service

# Power calculation
python -m cli.commands power --base 2 --exponent 10

# Fibonacci
python -m cli.commands fibonacci --number 20

# Factorial
python -m cli.commands factorial --number 5

# View history
python -m cli.commands history
python -m cli.commands history --limit 10
python -m cli.commands history --operation power

# Cache operations
python -m cli.commands cache-stats
python -m cli.commands clear-cache
```

### Method 2: Using math-cli (Requires pip install -e .)

#### From Scripts Directory (PowerShell)
```powershell
cd C:\Users\[YourUsername]\AppData\Roaming\Python\Python312\Scripts

# Note the .\ prefix required in PowerShell
.\math-cli power --base 2 --exponent 10
.\math-cli fibonacci --number 20
.\math-cli factorial --number 5
.\math-cli history
.\math-cli cache-stats
.\math-cli clear-cache
```

#### From Project Directory
```bash
# Using full path
C:\Users\[YourUsername]\AppData\Roaming\Python\Python312\Scripts\math-cli power --base 2 --exponent 10
```

## Web Interface

Interactive API documentation: http://localhost:8000/docs

## Testing Commands

```bash
# Run all tests
pytest tests/ -v

# Run specific test modules
pytest tests/test_api.py -v
pytest tests/test_services.py -v

# Check code quality
flake8 app/ cli/ tests/
```

## Direct API Calls

### Using curl (Windows Command Prompt)
```cmd
curl -X POST "http://localhost:8000/api/v1/calculate" -H "Content-Type: application/json" -d "{\"operation\": \"power\", \"value\": 2, \"exponent\": 10}"

curl -X POST "http://localhost:8000/api/v1/calculate" -H "Content-Type: application/json" -d "{\"operation\": \"fibonacci\", \"value\": 20}"

curl -X POST "http://localhost:8000/api/v1/calculate" -H "Content-Type: application/json" -d "{\"operation\": \"factorial\", \"value\": 5}"

curl "http://localhost:8000/api/v1/history?limit=5"

curl "http://localhost:8000/api/v1/cache/stats"
```

### Using PowerShell
```powershell
# Power calculation
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/calculate" -Method POST -ContentType "application/json" -Body '{"operation": "power", "value": 2, "exponent": 10}'

# Fibonacci
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/calculate" -Method POST -ContentType "application/json" -Body '{"operation": "fibonacci", "value": 20}'

# Factorial
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/calculate" -Method POST -ContentType "application/json" -Body '{"operation": "factorial", "value": 5}'

# View history
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/history?limit=5"

# Cache statistics
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/cache/stats"
```

## Docker Commands

```bash
# Build and run with Docker Compose
docker-compose up --build

# Stop containers
docker-compose down

# Build image
docker build -t math-operations .

# Run container
docker run -p 8000:8000 math-operations
```

## Installation Commands

```bash
# Install dependencies
pip install --user -r requirements.txt

# Install CLI tool
pip install --user -e .

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

## Quick Test Script

Create `test_all.bat` for Windows:
```batch
@echo off
echo Testing Power...
python -m cli.commands power --base 2 --exponent 10
timeout /t 1 >nul

echo Testing Fibonacci...
python -m cli.commands fibonacci --number 20
timeout /t 1 >nul

echo Testing Factorial...
python -m cli.commands factorial --number 5
timeout /t 1 >nul

echo Showing History...
python -m cli.commands history --limit 5
timeout /t 1 >nul

echo Cache Statistics...
python -m cli.commands cache-stats
```

Run with: `test_all.bat`

## PowerShell Note

In PowerShell, when running executables from the current directory, use the .\ prefix:
- Incorrect: `math-cli power --base 2 --exponent 10`
- Correct: `.\math-cli power --base 2 --exponent 10`
- Alternative: `python -m cli.commands power --base 2 --exponent 10`

## Common Operations Summary

| Task | Command |
|------|---------|
| Start API | `python run.py` |
| Calculate 2^10 | `python -m cli.commands power --base 2 --exponent 10` |
| Get 20th Fibonacci | `python -m cli.commands fibonacci --number 20` |
| Calculate 5! | `python -m cli.commands factorial --number 5` |
| View history | `python -m cli.commands history` |
| Cache statistics | `python -m cli.commands cache-stats` |
| Clear cache | `python -m cli.commands clear-cache` |
| Run tests | `pytest tests/ -v` |
| Check code quality | `flake8 app/` |
| API documentation | Open http://localhost:8000/docs |