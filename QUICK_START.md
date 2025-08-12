# Quick Start Guide

## Initial Setup

### Step 1: Install Dependencies
```bash
# Install with user flag
pip install --user -r requirements.txt

# Or use virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
# Copy example configuration
copy .env.example .env  # Windows
cp .env.example .env  # Linux/Mac
```

### Step 3: Install CLI Tool (Optional)
```bash
pip install --user -e .
```

## Running the Application

### Terminal 1 - Start API Server
```bash
python run.py
# Keep this running. API is available at http://localhost:8000
```

### Terminal 2 - Use the Service

#### Option A: Python Module (Recommended)
```bash
# Navigate to project directory
cd math-operations-service

# Run commands
python -m cli.commands power --base 2 --exponent 10
python -m cli.commands fibonacci --number 20
python -m cli.commands factorial --number 5
python -m cli.commands history --limit 10
python -m cli.commands cache-stats
python -m cli.commands clear-cache
```

#### Option B: Using math-cli Command
```bash
# From Scripts directory (PowerShell)
cd C:\Users\[YourUsername]\AppData\Roaming\Python\Python312\Scripts
.\math-cli power --base 2 --exponent 10
.\math-cli fibonacci --number 20

# From project directory (using full path)
C:\Users\[YourUsername]\AppData\Roaming\Python\Python312\Scripts\math-cli power --base 2 --exponent 10
```

#### Option C: Web Interface
Open browser at `http://localhost:8000/docs` for interactive API testing

## Testing the Application

```bash
# Run tests (in Terminal 2 while API runs in Terminal 1)
pytest tests/ -v

# Check code quality
flake8 app/ cli/ tests/
```

## Quick Command Reference

| Operation | Command |
|-----------|---------|
| Start API | `python run.py` |
| Power calculation | `python -m cli.commands power --base 2 --exponent 10` |
| Fibonacci | `python -m cli.commands fibonacci --number 20` |
| Factorial | `python -m cli.commands factorial --number 5` |
| View history | `python -m cli.commands history` |
| Cache statistics | `python -m cli.commands cache-stats` |
| Clear cache | `python -m cli.commands clear-cache` |
| Run tests | `pytest tests/ -v` |
| Check code | `flake8 app/` |

## Windows PowerShell Notes

PowerShell requires .\ prefix when running executables from current directory:
```powershell
# Wrong (in Scripts directory)
math-cli power --base 2 --exponent 10

# Correct (in Scripts directory)
.\math-cli power --base 2 --exponent 10

# Always works (from project directory)
python -m cli.commands power --base 2 --exponent 10
```

## Common Issues

### CLI Command Not Found
Use `python -m cli.commands` instead of `math-cli` - this always works from the project directory.

### Connection Refused
Ensure the API is running in Terminal 1 before using CLI commands.

### Module Not Found
Verify you're in the correct project directory and all files are properly placed.