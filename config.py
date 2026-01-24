"""
Configuration for Multi-Tool LLM Agent
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration.
    
    All configuration is loaded from environment variables via .env file.
    See .env.example for required variables.
    """
    
    # API Configuration
    AIPIPE_API_KEY = os.getenv("AIPIPE_API_KEY", "")
    AIPIPE_BASE_URL = os.getenv("AIPIPE_BASE_URL", "https://aipipe.org/openai/v1")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
    
    # Optional API Keys
    SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
    
    # LLM Settings
    MAX_TOKENS = 2000
    TEMPERATURE = 0.7
    
    # Agent Settings
    MAX_ITERATIONS = 10
    VERBOSE = True
    
    # Paths
    BASE_DIR = Path(__file__).parent
    UPLOAD_FOLDER = BASE_DIR / "uploaded_files"
    DATA_FOLDER = BASE_DIR / "data"
    VECTORSTORE_PATH = DATA_FOLDER / "vectorstore"
    
    # File Settings
    MAX_FILE_SIZE_MB = 10
    ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.docx', '.csv', '.json', '.py', '.md', '.log'}
    
    # RAG Settings
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    
    @classmethod
    def setup_directories(cls):
        """Create necessary directories if they don't exist.
        
        Ensures all required folders are created for file uploads, data storage, etc.
        """
        try:
            cls.UPLOAD_FOLDER.mkdir(exist_ok=True)
            cls.DATA_FOLDER.mkdir(exist_ok=True)
            cls.VECTORSTORE_PATH.mkdir(exist_ok=True)
        except Exception as e:
            raise RuntimeError(f"Failed to create directories: {str(e)}")
    
    @classmethod
    def validate(cls):
        """Validate configuration is complete and correct.
        
        Checks that required API keys are set and creates necessary directories.
        
        Returns:
            bool: True if configuration is valid
            
        Raises:
            ValueError: If required configuration is missing
        """
        if not cls.AIPIPE_API_KEY:
            raise ValueError(
                "❌ AIPIPE_API_KEY not set in .env file.\n"
                "Please:\n"
                "1. Copy .env.example to .env\n"
                "2. Add your AI Pipe API key from https://aipipe.org/login\n"
                "3. Save and restart the application"
            )
        cls.setup_directories()
        return True