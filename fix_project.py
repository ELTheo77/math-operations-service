"""Script to fix project structure and create missing files."""
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def create_directories():
    """Create necessary directories."""
    directories = [
        "app/models",
        "app/services", 
        "app/db",
        "data",
        "logs",
        "cli",
        "tests"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Directory created/verified: {dir_path}")

def create_file(path, content):
    """Create a file with given content."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding='utf-8')
    print(f"✓ File created: {path}")

def fix_project_structure():
    """Fix the entire project structure."""
    print("Fixing Math Operations Service project structure...\n")
    
    # Create directories
    print("Creating directories...")
    create_directories()
    print()
    
    # Create missing __init__.py files
    print("Creating __init__.py files...")
    init_paths = [
        "app/__init__.py",
        "app/api/__init__.py",
        "app/core/__init__.py",
        "app/models/__init__.py",
        "app/services/__init__.py",
        "app/db/__init__.py",
        "app/utils/__init__.py",
        "cli/__init__.py",
        "tests/__init__.py"
    ]
    
    for path in init_paths:
        if not Path(path).exists():
            create_file(path, '"""Package initialization."""')
    print()
    
    # Create .env file if it doesn't exist
    if not Path(".env").exists():
        print("Creating .env file...")
        env_content = """# Application Configuration
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
BACKEND_CORS_ORIGINS=["*"]"""
        create_file(".env", env_content)
    else:
        print("✓ .env file already exists")
    
    print()
    
    # Check if required files exist in correct locations
    print("Checking file locations...")
    required_files = {
        "app/models/schemas.py": "Pydantic schemas",
        "app/models/database.py": "Database models",
        "app/services/calculator.py": "Calculator service",
        "app/services/cache.py": "Cache service",
        "app/db/base.py": "Database configuration",
        "app/db/session.py": "Session management"
    }
    
    missing_files = []
    for file_path, description in required_files.items():
        if Path(file_path).exists():
            print(f"✓ {description}: {file_path}")
        else:
            print(f"✗ Missing {description}: {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠ Warning: {len(missing_files)} required files are missing!")
        print("Please ensure all files from the artifacts are saved in the correct locations.")
        print("\nMissing files:")
        for file in missing_files:
            print(f"  - {file}")
    
    print("\n" + "="*50)
    print("Project structure check complete!")
    
    if not missing_files:
        print("\n✅ All files are in place! You can now run:")
        print("   python run.py")
        print("\nOr use uvicorn directly:")
        print("   uvicorn app.main:app --reload")
    else:
        print("\n⚠ Please copy the missing files from the artifacts above to their correct locations.")
        print("After copying the files, run this script again to verify.")
    
    # Add Scripts to PATH for Windows
    if sys.platform == "win32":
        scripts_path = r"C:\\Users\\Teo\\AppData\\Roaming\\Python\\Python312\\Scripts"
        if scripts_path not in os.environ.get('PATH', ''):
            print(f"\n💡 Tip: Add {scripts_path} to your PATH to use uvicorn command directly")

if __name__ == "__main__":
    try:
        fix_project_structure()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    
    print("\nPress Enter to exit...")
    input()