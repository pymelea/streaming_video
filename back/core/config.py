import os
from dotenv import load_dotenv
from pydantic import BaseSettings

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    # API configuration
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Stream API"
    
    # Database configuration
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'postgresql+psycopg2://streamapp:mylov2@localhost:5432/streamapp')
    
    # OMDB API configuration
    OMDB_API_KEY: str = os.getenv('OMDB_API_KEY', '')
    
    # File storage configuration
    UPLOAD_DIR: str = "uploads"
    VIDEOS_DIR: str = os.path.join(UPLOAD_DIR, "videos")
    SUBTITLES_DIR: str = os.path.join(UPLOAD_DIR, "subtitles")
    THUMBNAILS_DIR: str = os.path.join(UPLOAD_DIR, "thumbnails")
    
    # CORS configuration
    CORS_ORIGINS: list = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:3000",
        "*"
    ]
    
    class Config:
        case_sensitive = True

# Create settings instance
settings = Settings()

# Ensure upload directories exist
os.makedirs(settings.VIDEOS_DIR, exist_ok=True)
os.makedirs(settings.SUBTITLES_DIR, exist_ok=True)
os.makedirs(settings.THUMBNAILS_DIR, exist_ok=True)
