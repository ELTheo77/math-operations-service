@echo off
echo Fixing Math Operations Service project structure...
echo.

REM Create necessary directories
echo Creating directories...
if not exist "app\models" mkdir "app\models"
if not exist "app\services" mkdir "app\services"
if not exist "app\db" mkdir "app\db"
if not exist "data" mkdir "data"
if not exist "logs" mkdir "logs"

echo.
echo Directories created successfully!
echo.

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy ".env.example" ".env" 2>nul || (
        echo # Application Configuration > .env
        echo PROJECT_NAME="Math Operations Microservice" >> .env
        echo VERSION="1.0.0" >> .env
        echo API_V1_STR="/api/v1" >> .env
        echo. >> .env
        echo # Server Configuration >> .env
        echo HOST="0.0.0.0" >> .env
        echo PORT=8000 >> .env
        echo. >> .env
        echo # Database Configuration >> .env
        echo DATABASE_URL="sqlite+aiosqlite:///data/math_operations.db" >> .env
        echo. >> .env
        echo # Cache Configuration >> .env
        echo CACHE_TTL_SECONDS=3600 >> .env
        echo CACHE_MAX_SIZE=1000 >> .env
        echo. >> .env
        echo # Logging >> .env
        echo LOG_LEVEL="INFO" >> .env
    )
    echo .env file created!
)

echo.
echo Adding Python Scripts directory to PATH for current session...
set PATH=%PATH%;C:\Users\Teo\AppData\Roaming\Python\Python312\Scripts

echo.
echo Project structure fixed!
echo.
echo You can now run the application with:
echo   python run.py
echo.
echo Or use uvicorn directly:
echo   uvicorn app.main:app --reload
echo.
pause