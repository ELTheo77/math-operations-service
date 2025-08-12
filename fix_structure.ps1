# PowerShell script to fix Math Operations Service project structure

Write-Host "Fixing Math Operations Service project structure..." -ForegroundColor Green
Write-Host ""

# Create necessary directories
Write-Host "Creating directories..." -ForegroundColor Yellow
$directories = @("app\models", "app\services", "app\db", "data", "logs")

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  Created: $dir" -ForegroundColor Cyan
    } else {
        Write-Host "  Exists: $dir" -ForegroundColor DarkGray
    }
}

Write-Host ""
Write-Host "Directories ready!" -ForegroundColor Green
Write-Host ""

# Create .env file if it doesn't exist
if (!(Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
    } else {
        @"
# Application Configuration
PROJECT_NAME="Math Operations Microservice"
VERSION="1.0.0"
API_V1_STR="/api/v1"

# Server Configuration
HOST="0.0.0.0"
PORT=8000

# Database Configuration
DATABASE_URL="sqlite+aiosqlite:///data/math_operations.db"

# Cache Configuration
CACHE_TTL_SECONDS=3600
CACHE_MAX_SIZE=1000

# Logging
LOG_LEVEL="INFO"

# CORS
BACKEND_CORS_ORIGINS=["*"]
"@ | Out-File -FilePath ".env" -Encoding UTF8
    }
    Write-Host ".env file created!" -ForegroundColor Green
} else {
    Write-Host ".env file already exists" -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "Adding Python Scripts directory to PATH for current session..." -ForegroundColor Yellow
$env:PATH += ";C:\Users\Teo\AppData\Roaming\Python\Python312\Scripts"

Write-Host ""
Write-Host "Project structure fixed!" -ForegroundColor Green
Write-Host ""
Write-Host "You can now run the application with:" -ForegroundColor Cyan
Write-Host "  python run.py" -ForegroundColor White
Write-Host ""
Write-Host "Or use uvicorn directly:" -ForegroundColor Cyan
Write-Host "  uvicorn app.main:app --reload" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")