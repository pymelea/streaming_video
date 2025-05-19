import pytest
import os
import json
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Import the application and database components
from db.database import Base
from services.video_service import VideoService
from services.playlist_service import PlaylistService
from models.video import Video
from models.playlist import Playlist
from models.category import Category
from models.subtitle import Subtitle
from core.config import settings

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_services.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    # Drop tables
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def setup_test_dirs():
    # Crear directorios necesarios para las pruebas
    os.makedirs("uploads/videos", exist_ok=True)
    os.makedirs("uploads/subtitles", exist_ok=True)
    os.makedirs("uploads/thumbnails", exist_ok=True)
    
    yield
    
    # Limpiar archivos después de las pruebas
    for file in os.listdir("uploads/videos"):
        if file != ".gitkeep" and not os.path.isdir(os.path.join("uploads/videos", file)):
            os.remove(os.path.join("uploads/videos", file))
    
    for file in os.listdir("uploads/subtitles"):
        if file != ".gitkeep" and not os.path.isdir(os.path.join("uploads/subtitles", file)):
            os.remove(os.path.join("uploads/subtitles", file))
            
    for file in os.listdir("uploads/thumbnails"):
        if file != ".gitkeep" and not os.path.isdir(os.path.join("uploads/thumbnails", file)):
            os.remove(os.path.join("uploads/thumbnails", file))

@pytest.fixture
def video_service():
    return VideoService()

@pytest.fixture
def playlist_service():
    return PlaylistService()

def test_video_service_map_video_to_schema(video_service):
    # Create a mock video object
    video = MagicMock()
    video.id = 1
    video.title = "Test Video"
    video.upload_date = datetime.now()
    video.imdb_id = "tt1234567"
    video.filename = "test.mp4"
    video.year = 2023
    video.duration = 120
    video.thumbnail = "test.jpg"
    video.description = "Test description"
    
    # Mock categories
    category = MagicMock()
    category.name = "Action"
    video.categories = [category]
    
    # Mock subtitles
    subtitle = MagicMock()
    subtitle.id = 1
    subtitle.filename = "test.srt"
    video.subtitles = [subtitle]
    
    # Call the method
    result = video_service._map_video_to_schema(video)
    
    # Verify the result
    assert result["id"] == 1
    assert result["title"] == "Test Video"
    assert result["imdb_id"] == "tt1234567"
    assert result["filename"] == "test.mp4"
    assert result["year"] == 2023
    assert result["duration"] == 120
    assert result["thumbnail"] == "test.jpg"
    assert result["description"] == "Test description"
    assert result["categories"] == ["Action"]
    assert result["stream_url"] == f"{settings.API_V1_STR}/videos/stream/1"
    assert result["subtitles_urls"] == [f"{settings.API_V1_STR}/subtitles/content/1"]

def test_playlist_service_map_playlist_to_schema(playlist_service):
    # Create a mock playlist object
    playlist = MagicMock()
    playlist.id = 1
    playlist.name = "Test Playlist"
    playlist.description = "Test description"
    
    # Mock videos
    video = MagicMock()
    video.id = 1
    video.title = "Test Video"
    video.upload_date = datetime.now()
    video.imdb_id = "tt1234567"
    video.filename = "test.mp4"
    video.year = 2023
    video.duration = 120
    video.thumbnail = "test.jpg"
    video.description = "Test description"
    video.categories = []
    video.subtitles = []
    playlist.videos = [video]
    
    # Call the method
    result = playlist_service._map_playlist_to_schema(playlist)
    
    # Verify the result
    assert result["id"] == 1
    assert result["name"] == "Test Playlist"
    assert result["description"] == "Test description"
    assert len(result["videos"]) == 1
    assert result["videos"][0]["id"] == 1
    assert result["videos"][0]["title"] == "Test Video"

def test_playlist_service_get_playlist_videos(playlist_service, test_db):
    # Create a mock playlist with videos
    with patch.object(test_db, 'query') as mock_query:
        # Mock the query result
        mock_playlist = MagicMock()
        mock_playlist.id = 1
        mock_playlist.name = "Test Playlist"
        mock_playlist.description = "Test description"
        
        # Mock videos
        mock_video = MagicMock()
        mock_video.id = 1
        mock_video.title = "Test Video"
        mock_video.upload_date = datetime.now()
        mock_video.imdb_id = "tt1234567"
        mock_video.filename = "test.mp4"
        mock_video.year = 2023
        mock_video.duration = 120
        mock_video.thumbnail = "test.jpg"
        mock_video.description = "Test description"
        mock_video.categories = []
        mock_video.subtitles = []
        mock_playlist.videos = [mock_video]
        
        # Configure the mock
        mock_filter = MagicMock()
        mock_filter.first.return_value = mock_playlist
        mock_query.return_value.filter.return_value = mock_filter
        
        # Call the method
        result = playlist_service.get_playlist_videos(test_db, playlist_id=1)
        
        # Verify the result
        assert len(result) == 1
        assert result[0]["id"] == 1
        assert result[0]["title"] == "Test Video"
        assert result[0]["stream_url"] == f"{settings.API_V1_STR}/videos/stream/1"

def test_playlist_service_get_playlist_videos_not_found(playlist_service, test_db):
    # Test getting videos from a non-existent playlist
    with patch.object(test_db, 'query') as mock_query:
        # Configure the mock to return None
        mock_filter = MagicMock()
        mock_filter.first.return_value = None
        mock_query.return_value.filter.return_value = mock_filter
        
        # Call the method
        result = playlist_service.get_playlist_videos(test_db, playlist_id=999)
        
        # Verify the result
        assert result is None
