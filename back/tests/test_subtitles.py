import pytest
import os
import shutil
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, mock_open
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Import the application and database components
from main import app
from db.database import Base, get_db

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

# Ensure the test directories exist
@pytest.fixture(scope="function")
def setup_test_dirs():
    # Create necessary directories for tests
    os.makedirs("uploads/subtitles", exist_ok=True)
    
    yield
    
    # Clean up files after tests
    for file in os.listdir("uploads/subtitles"):
        if file != ".gitkeep":
            os.remove(os.path.join("uploads/subtitles", file))


def test_get_subtitle_content(client, test_db, monkeypatch, setup_test_dirs):
    # Create a test subtitle file
    test_subtitle_path = "uploads/subtitles/test_subtitle.srt"
    subtitle_content = """1
00:00:00,000 --> 00:00:05,000
Hello, this is a test subtitle"""
    
    with open(test_subtitle_path, "w") as f:
        f.write(subtitle_content)
    
    # Mock the query to return a subtitle
    def mock_query_filter(*args, **kwargs):
        mock = MagicMock()
        subtitle = MagicMock()
        subtitle.id = 1
        subtitle.filename = "test_subtitle.srt"
        mock.first.return_value = subtitle
        return mock
    
    # Apply the mock
    monkeypatch.setattr("sqlalchemy.orm.Query.filter", mock_query_filter)
    
    # Make the request
    response = client.get("/api/subtitles/content/1")
    
    # Verify the response
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/x-subrip"
    assert "content-disposition" in response.headers
    assert response.content.decode() == subtitle_content


def test_get_nonexistent_subtitle(client, test_db, monkeypatch):
    # Mock the query to return None (subtitle not found)
    def mock_query_filter_none(*args, **kwargs):
        mock = MagicMock()
        mock.first.return_value = None
        return mock
    
    # Apply the mock
    monkeypatch.setattr("sqlalchemy.orm.Query.filter", mock_query_filter_none)
    
    # Make the request
    response = client.get("/api/subtitles/content/999")
    
    # Verify that it returns a 404
    assert response.status_code == 404
    assert response.json()["detail"] == "Subtitle not found"


def test_get_subtitle_file_not_found(client, test_db, monkeypatch):
    # Mock the query to return a subtitle
    def mock_query_filter(*args, **kwargs):
        mock = MagicMock()
        subtitle = MagicMock()
        subtitle.id = 1
        subtitle.filename = "nonexistent_subtitle.srt"
        mock.first.return_value = subtitle
        return mock
    
    # Mock os.path.exists to return False
    def mock_exists(path):
        return False
    
    # Apply the mocks
    monkeypatch.setattr("sqlalchemy.orm.Query.filter", mock_query_filter)
    monkeypatch.setattr("os.path.exists", mock_exists)
    
    # Make the request
    response = client.get("/api/subtitles/content/1")
    
    # Verify that it returns a 404
    assert response.status_code == 404
    assert response.json()["detail"] == "Subtitle file not found"


def test_get_subtitle_srt_format(client, test_db, monkeypatch, setup_test_dirs):
    # Test SRT subtitle format
    filename = "test_subtitle.srt"
    test_subtitle_path = f"uploads/subtitles/{filename}"
    subtitle_content = "Test subtitle content"
    
    with open(test_subtitle_path, "w") as f:
        f.write(subtitle_content)
    
    # Mock the query to return a subtitle with SRT format
    def mock_query_filter(*args, **kwargs):
        mock = MagicMock()
        subtitle = MagicMock()
        subtitle.id = 1
        subtitle.filename = filename
        mock.first.return_value = subtitle
        return mock
    
    # Apply the mock
    monkeypatch.setattr("sqlalchemy.orm.Query.filter", mock_query_filter)
    
    # Make the request
    response = client.get("/api/subtitles/content/1")
    
    # Verify the response
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/x-subrip"
    assert "content-disposition" in response.headers
    assert response.content.decode() == subtitle_content


def test_get_subtitle_vtt_format(client, test_db, monkeypatch, setup_test_dirs):
    # Test VTT subtitle format
    filename = "test_subtitle.vtt"
    test_subtitle_path = f"uploads/subtitles/{filename}"
    subtitle_content = "Test subtitle content"
    
    with open(test_subtitle_path, "w") as f:
        f.write(subtitle_content)
    
    # Mock the query to return a subtitle with VTT format
    def mock_query_filter(*args, **kwargs):
        mock = MagicMock()
        subtitle = MagicMock()
        subtitle.id = 1
        subtitle.filename = filename
        mock.first.return_value = subtitle
        return mock
    
    # Apply the mock
    monkeypatch.setattr("sqlalchemy.orm.Query.filter", mock_query_filter)
    
    # Make the request
    response = client.get("/api/subtitles/content/1")
    
    # Verify the response
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/vtt")  # Accept any charset
    assert "content-disposition" in response.headers
    assert response.content.decode() == subtitle_content


def test_get_subtitle_unknown_format(client, test_db, monkeypatch, setup_test_dirs):
    # Test unknown subtitle format (should default to text/plain)
    filename = "test_subtitle.xyz"
    test_subtitle_path = f"uploads/subtitles/{filename}"
    subtitle_content = "Test subtitle content"
    
    with open(test_subtitle_path, "w") as f:
        f.write(subtitle_content)
    
    # Mock the query to return a subtitle with unknown format
    def mock_query_filter(*args, **kwargs):
        mock = MagicMock()
        subtitle = MagicMock()
        subtitle.id = 1
        subtitle.filename = filename
        mock.first.return_value = subtitle
        return mock
    
    # Apply the mock
    monkeypatch.setattr("sqlalchemy.orm.Query.filter", mock_query_filter)
    
    # Make the request
    response = client.get("/api/subtitles/content/1")
    
    # Verify the response
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")  # Accept any charset
    assert "content-disposition" in response.headers
    assert response.content.decode() == subtitle_content
