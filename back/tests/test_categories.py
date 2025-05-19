import pytest
import os
import shutil
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, mock_open
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime

# Import the application and database components
from main import app
from db.database import Base, get_db
from models.category import Category

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def test_app():
    # Override the dependency
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return app

@pytest.fixture(scope="session")
def client(test_app):
    return TestClient(test_app)

@pytest.fixture(scope="function")
def test_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables
    Base.metadata.drop_all(bind=engine)

# Test fixture to create sample categories
@pytest.fixture(scope="function")
def sample_categories(test_db):
    # Create a session
    db = TestingSessionLocal()
    
    # Create sample categories
    categories = [
        Category(name="Action", description="Action movies"),
        Category(name="Comedy", description="Comedy movies"),
        Category(name="Drama", description="Drama movies"),
        Category(name="Sci-Fi", description="Science Fiction movies")
    ]
    
    # Add categories to the database
    for category in categories:
        db.add(category)
    
    db.commit()
    
    # Refresh categories to get their IDs
    for category in categories:
        db.refresh(category)
    
    yield categories
    
    # Clean up
    db.close()


def test_categories_in_video_response(client, test_db, monkeypatch):
    # Test that categories are properly included in video responses
    # Mock the database query to return a test video with categories
    def mock_query_filter(*args, **kwargs):
        mock = MagicMock()
        video = MagicMock()
        video.id = 1
        video.title = "Test Movie"
        video.filename = "test_movie.mp4"
        video.upload_date = datetime.now()  # Use actual datetime object
        video.imdb_id = "tt1234567"
        video.year = 2023
        video.duration = 120
        video.thumbnail = "thumbnail.jpg"
        video.description = "A test movie description"
        
        # Create mock categories
        category1 = MagicMock()
        category1.name = "Action"
        category2 = MagicMock()
        category2.name = "Adventure"
        video.categories = [category1, category2]
        
        # Create mock subtitles
        subtitle = MagicMock()
        subtitle.id = 1
        subtitle.filename = "test_subtitle.srt"
        video.subtitles = [subtitle]
        
        mock.first.return_value = video
        return mock
    
    # Apply the mock
    monkeypatch.setattr("sqlalchemy.orm.Query.filter", mock_query_filter)
    
    # Make the request to get a video
    response = client.get("/api/videos/1")
    
    # Verify the response
    assert response.status_code == 200
    data = response.json()
    
    # Check that categories are included in the response
    assert "categories" in data
    assert isinstance(data["categories"], list)
    assert "Action" in data["categories"]
    assert "Adventure" in data["categories"]


def test_categories_in_video_list(client, test_db, monkeypatch):
    # Test that categories are properly included in video list responses
    # Mock the database query to return a list of videos with categories
    def mock_query(*args, **kwargs):
        mock = MagicMock()
        
        # Create a mock video with categories
        video1 = MagicMock()
        video1.id = 1
        video1.title = "Test Movie 1"
        video1.filename = "test_movie1.mp4"
        video1.upload_date = datetime.now()  # Use actual datetime object
        video1.imdb_id = "tt1234567"
        video1.year = 2023
        video1.duration = 120
        video1.thumbnail = "thumbnail1.jpg"
        video1.description = "A test movie description"
        
        # Create mock categories for video1
        category1 = MagicMock()
        category1.name = "Action"
        category2 = MagicMock()
        category2.name = "Adventure"
        video1.categories = [category1, category2]
        
        # Create mock subtitles for video1
        subtitle1 = MagicMock()
        subtitle1.id = 1
        subtitle1.filename = "test_subtitle1.srt"
        video1.subtitles = [subtitle1]
        
        # Create a second mock video with different categories
        video2 = MagicMock()
        video2.id = 2
        video2.title = "Test Movie 2"
        video2.filename = "test_movie2.mp4"
        video2.upload_date = datetime.now()  # Use actual datetime object
        video2.imdb_id = "tt7654321"
        video2.year = 2023
        video2.duration = 110
        video2.thumbnail = "thumbnail2.jpg"
        video2.description = "Another test movie description"
        
        # Create mock categories for video2
        category3 = MagicMock()
        category3.name = "Comedy"
        category4 = MagicMock()
        category4.name = "Drama"
        video2.categories = [category3, category4]
        
        # Create mock subtitles for video2
        subtitle2 = MagicMock()
        subtitle2.id = 2
        subtitle2.filename = "test_subtitle2.srt"
        video2.subtitles = [subtitle2]
        
        # Configure the mock to return both videos
        mock.offset.return_value = mock
        mock.limit.return_value = mock
        mock.all.return_value = [video1, video2]
        
        return mock
    
    # Apply the mock
    monkeypatch.setattr("sqlalchemy.orm.Session.query", mock_query)
    
    # Make the request to list videos
    response = client.get("/api/videos/")
    
    # Verify the response
    assert response.status_code == 200
    data = response.json()
    
    # Check that we have two videos in the response
    assert len(data) == 2
    
    # Check that categories are included in each video
    assert "categories" in data[0]
    assert isinstance(data[0]["categories"], list)
    assert "Action" in data[0]["categories"]
    assert "Adventure" in data[0]["categories"]
    
    assert "categories" in data[1]
    assert isinstance(data[1]["categories"], list)
    assert "Comedy" in data[1]["categories"]
    assert "Drama" in data[1]["categories"]
