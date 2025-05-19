import pytest
import os
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Import the application and database components
from main import app
from db.database import Base, get_db
from services.playlist_service import playlist_service

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_playlists.db"
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

def test_list_playlists(client, test_db, monkeypatch):
    # Mock the playlist service
    def mock_list_playlists(*args, **kwargs):
        return [
            {
                "id": 1,
                "name": "Test Playlist",
                "description": "Test description",
                "videos": [
                    {
                        "id": 1,
                        "title": "Test Video",
                        "upload_date": datetime.now().isoformat(),
                        "categories": ["Action"],
                        "imdb_id": "tt1234567",
                        "filename": "test.mp4",
                        "stream_url": "/api/videos/stream/1",
                        "year": 2023,
                        "duration": 120,
                        "thumbnail": "test.jpg",
                        "description": "Test description",
                        "subtitles_urls": ["/api/subtitles/content/1"]
                    }
                ]
            }
        ]
    
    # Apply the mock
    monkeypatch.setattr(playlist_service, "list_playlists", mock_list_playlists)
    
    # Make the request
    response = client.get("/api/playlists/")
    
    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Playlist"
    assert len(data[0]["videos"]) == 1
    assert data[0]["videos"][0]["title"] == "Test Video"

def test_get_playlist(client, test_db, monkeypatch):
    # Mock the playlist service
    def mock_get_playlist(*args, **kwargs):
        return {
            "id": 1,
            "name": "Test Playlist",
            "description": "Test description",
            "videos": [
                {
                    "id": 1,
                    "title": "Test Video",
                    "upload_date": datetime.now().isoformat(),
                    "categories": ["Action"],
                    "imdb_id": "tt1234567",
                    "filename": "test.mp4",
                    "stream_url": "/api/videos/stream/1",
                    "year": 2023,
                    "duration": 120,
                    "thumbnail": "test.jpg",
                    "description": "Test description",
                    "subtitles_urls": ["/api/subtitles/content/1"]
                }
            ]
        }
    
    # Apply the mock
    monkeypatch.setattr(playlist_service, "get_playlist", mock_get_playlist)
    
    # Make the request
    response = client.get("/api/playlists/1")
    
    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Playlist"
    assert len(data["videos"]) == 1
    assert data["videos"][0]["title"] == "Test Video"

def test_get_playlist_not_found(client, test_db, monkeypatch):
    # Mock the playlist service to return None
    def mock_get_playlist_none(*args, **kwargs):
        return None
    
    # Apply the mock
    monkeypatch.setattr(playlist_service, "get_playlist", mock_get_playlist_none)
    
    # Make the request
    response = client.get("/api/playlists/999")
    
    # Verify the response
    assert response.status_code == 404
    assert response.json()["detail"] == "Playlist not found"

def test_get_playlist_videos(client, test_db, monkeypatch):
    # Mock the playlist service
    def mock_get_playlist_videos(*args, **kwargs):
        return [
            {
                "id": 1,
                "title": "Test Video",
                "upload_date": datetime.now().isoformat(),
                "categories": ["Action"],
                "imdb_id": "tt1234567",
                "filename": "test.mp4",
                "stream_url": "/api/videos/stream/1",
                "year": 2023,
                "duration": 120,
                "thumbnail": "test.jpg",
                "description": "Test description",
                "subtitles_urls": ["/api/subtitles/content/1"]
            }
        ]
    
    # Apply the mock
    monkeypatch.setattr(playlist_service, "get_playlist_videos", mock_get_playlist_videos)
    
    # Make the request
    response = client.get("/api/playlists/1/videos")
    
    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Video"
    assert data[0]["stream_url"] == "/api/videos/stream/1"

def test_get_playlist_videos_not_found(client, test_db, monkeypatch):
    # Mock the playlist service to return None
    def mock_get_playlist_videos_none(*args, **kwargs):
        return None
    
    # Apply the mock
    monkeypatch.setattr(playlist_service, "get_playlist_videos", mock_get_playlist_videos_none)
    
    # Make the request
    response = client.get("/api/playlists/999/videos")
    
    # Verify the response
    assert response.status_code == 404
    assert response.json()["detail"] == "Playlist not found"

def test_create_playlist(client, test_db, monkeypatch):
    # Mock the playlist repository and service
    def mock_get_by_name(*args, **kwargs):
        return None
    
    def mock_create_playlist(*args, **kwargs):
        return {
            "id": 1,
            "name": "New Playlist",
            "description": "New description",
            "videos": []
        }
    
    # Apply the mocks
    from db.repositories.playlist_repository import playlist_repository
    monkeypatch.setattr(playlist_repository, "get_by_name", mock_get_by_name)
    monkeypatch.setattr(playlist_service, "create_playlist", mock_create_playlist)
    
    # Make the request
    response = client.post(
        "/api/playlists/",
        json={
            "name": "New Playlist",
            "description": "New description"
        }
    )
    
    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Playlist"
    assert data["description"] == "New description"

def test_update_playlist(client, test_db, monkeypatch):
    # Mock the playlist repository and service
    def mock_get(*args, **kwargs):
        mock_playlist = MagicMock()
        mock_playlist.id = 1
        mock_playlist.name = "Test Playlist"
        mock_playlist.description = "Test description"
        return mock_playlist
    
    def mock_update_playlist(*args, **kwargs):
        return {
            "id": 1,
            "name": "Updated Playlist",
            "description": "Updated description",
            "videos": []
        }
    
    # Apply the mocks
    from db.repositories.playlist_repository import playlist_repository
    monkeypatch.setattr(playlist_repository, "get", mock_get)
    monkeypatch.setattr(playlist_service, "update_playlist", mock_update_playlist)
    
    # Make the request
    response = client.put(
        "/api/playlists/1",
        json={
            "name": "Updated Playlist",
            "description": "Updated description"
        }
    )
    
    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Playlist"
    assert data["description"] == "Updated description"

def test_update_playlist_not_found(client, test_db, monkeypatch):
    # Mock the playlist repository to return None
    def mock_get_none(*args, **kwargs):
        return None
    
    # Apply the mock
    from db.repositories.playlist_repository import playlist_repository
    monkeypatch.setattr(playlist_repository, "get", mock_get_none)
    
    # Make the request
    response = client.put(
        "/api/playlists/999",
        json={
            "name": "Updated Playlist",
            "description": "Updated description"
        }
    )
    
    # Verify the response
    assert response.status_code == 404
    assert response.json()["detail"] == "Playlist not found"

def test_delete_playlist(client, test_db, monkeypatch):
    # Mock the playlist service and repository
    def mock_get_playlist(*args, **kwargs):
        return {
            "id": 1,
            "name": "Test Playlist",
            "description": "Test description",
            "videos": []
        }
    
    def mock_remove(*args, **kwargs):
        return {
            "id": 1,
            "name": "Test Playlist",
            "description": "Test description",
            "videos": []
        }
    
    # Apply the mocks
    monkeypatch.setattr(playlist_service, "get_playlist", mock_get_playlist)
    from db.repositories.playlist_repository import playlist_repository
    monkeypatch.setattr(playlist_repository, "remove", mock_remove)
    
    # Make the request
    response = client.delete("/api/playlists/1")
    
    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Playlist"

def test_delete_playlist_not_found(client, test_db, monkeypatch):
    # Mock the playlist service to return None
    def mock_get_playlist_none(*args, **kwargs):
        return None
    
    # Apply the mock
    monkeypatch.setattr(playlist_service, "get_playlist", mock_get_playlist_none)
    
    # Make the request
    response = client.delete("/api/playlists/999")
    
    # Verify the response
    assert response.status_code == 404
    assert response.json()["detail"] == "Playlist not found"
