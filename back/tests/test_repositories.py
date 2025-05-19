import pytest
import os
from unittest.mock import patch, MagicMock
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Import the application and database components
from db.database import Base
from db.repositories.video_repository import VideoRepository
from db.repositories.playlist_repository import PlaylistRepository
from db.repositories.category_repository import CategoryRepository
from db.repositories.subtitle_repository import SubtitleRepository
from models.video import Video
from models.playlist import Playlist
from models.category import Category
from models.subtitle import Subtitle

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_repositories.db"
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

@pytest.fixture
def video_repository():
    return VideoRepository()

@pytest.fixture
def playlist_repository():
    return PlaylistRepository()

@pytest.fixture
def category_repository():
    return CategoryRepository()

@pytest.fixture
def subtitle_repository():
    return SubtitleRepository()

# Tests for VideoRepository
def test_video_repository_get_by_imdb_id(video_repository, test_db):
    # Create a test video
    test_video = Video(
        title="Test Video",
        imdb_id="tt1234567",
        filename="test.mp4",
        content_type="video/mp4"
    )
    test_db.add(test_video)
    test_db.commit()
    
    # Test getting the video by IMDB ID
    video = video_repository.get_by_imdb_id(test_db, imdb_id="tt1234567")
    
    # Verify the result
    assert video is not None
    assert video.title == "Test Video"
    assert video.imdb_id == "tt1234567"

def test_video_repository_get_with_categories(video_repository, test_db):
    # Create a test video
    test_video = Video(
        title="Test Video",
        imdb_id="tt1234567",
        filename="test.mp4",
        content_type="video/mp4"
    )
    test_db.add(test_video)
    test_db.commit()
    
    # Create a test category
    test_category = Category(
        name="Action"
    )
    test_db.add(test_category)
    test_db.commit()
    
    # Add the category to the video
    test_video.categories.append(test_category)
    test_db.commit()
    
    # Test getting the video with categories
    video = video_repository.get_with_categories(test_db, video_id=test_video.id)
    
    # Verify the result
    assert video is not None
    assert video.title == "Test Video"
    assert len(video.categories) == 1
    assert video.categories[0].name == "Action"

def test_video_repository_get_with_subtitles(video_repository, test_db):
    # Create a test video
    test_video = Video(
        title="Test Video",
        imdb_id="tt1234567",
        filename="test.mp4",
        content_type="video/mp4"
    )
    test_db.add(test_video)
    test_db.commit()
    
    # Create a test subtitle
    test_subtitle = Subtitle(
        video_id=test_video.id,
        filename="test.srt",
        language="en"
    )
    test_db.add(test_subtitle)
    test_db.commit()
    
    # Test getting the video with subtitles
    video = video_repository.get_with_subtitles(test_db, video_id=test_video.id)
    
    # Verify the result
    assert video is not None
    assert video.title == "Test Video"
    assert len(video.subtitles) == 1
    assert video.subtitles[0].filename == "test.srt"

def test_video_repository_create_with_categories(video_repository, test_db):
    # Create a test category
    test_category = Category(
        name="Action"
    )
    test_db.add(test_category)
    test_db.commit()
    
    # Test creating a video with categories
    video_data = {
        "title": "Test Video",
        "imdb_id": "tt1234567",
        "filename": "test.mp4",
        "content_type": "video/mp4"
    }
    
    video = video_repository.create_with_categories(
        test_db,
        obj_in=video_data,
        categories=[test_category]
    )
    
    # Verify the result
    assert video is not None
    assert video.title == "Test Video"
    assert video.imdb_id == "tt1234567"
    assert len(video.categories) == 1
    assert video.categories[0].name == "Action"

# Tests for PlaylistRepository
def test_playlist_repository_get_by_name(playlist_repository, test_db):
    # Create a test playlist
    test_playlist = Playlist(
        name="Test Playlist",
        description="Test description"
    )
    test_db.add(test_playlist)
    test_db.commit()
    
    # Test getting the playlist by name
    playlist = playlist_repository.get_by_name(test_db, name="Test Playlist")
    
    # Verify the result
    assert playlist is not None
    assert playlist.name == "Test Playlist"
    assert playlist.description == "Test description"

def test_playlist_repository_get_or_create_existing(playlist_repository, test_db):
    # Create a test playlist
    test_playlist = Playlist(
        name="Test Playlist",
        description="Test description"
    )
    test_db.add(test_playlist)
    test_db.commit()
    
    # Test getting an existing playlist
    playlist = playlist_repository.get_or_create(test_db, name="Test Playlist")
    
    # Verify the result
    assert playlist is not None
    assert playlist.name == "Test Playlist"
    assert playlist.description == "Test description"

def test_playlist_repository_get_or_create_new(playlist_repository, test_db):
    # Test creating a new playlist
    playlist = playlist_repository.get_or_create(test_db, name="New Playlist")
    
    # Verify the result
    assert playlist is not None
    assert playlist.name == "New Playlist"

def test_playlist_repository_get_multiple_by_names(playlist_repository, test_db):
    # Create test playlists
    test_playlist1 = Playlist(
        name="Test Playlist 1",
        description="Test description 1"
    )
    test_db.add(test_playlist1)
    
    test_playlist2 = Playlist(
        name="Test Playlist 2",
        description="Test description 2"
    )
    test_db.add(test_playlist2)
    test_db.commit()
    
    # Test getting multiple playlists by names
    playlists = playlist_repository.get_multiple_by_names(
        test_db,
        names=["Test Playlist 1", "Test Playlist 2", "New Playlist"]
    )
    
    # Verify the result
    assert len(playlists) == 3
    assert playlists[0].name == "Test Playlist 1"
    assert playlists[1].name == "Test Playlist 2"
    assert playlists[2].name == "New Playlist"

# Tests for CategoryRepository
def test_category_repository_get_by_name(category_repository, test_db):
    # Create a test category
    test_category = Category(
        name="Action"
    )
    test_db.add(test_category)
    test_db.commit()
    
    # Test getting the category by name
    category = category_repository.get_by_name(test_db, name="Action")
    
    # Verify the result
    assert category is not None
    assert category.name == "Action"

def test_category_repository_get_or_create_existing(category_repository, test_db):
    # Create a test category
    test_category = Category(
        name="Action"
    )
    test_db.add(test_category)
    test_db.commit()
    
    # Test getting an existing category
    category = category_repository.get_or_create(test_db, name="Action")
    
    # Verify the result
    assert category is not None
    assert category.name == "Action"

def test_category_repository_get_or_create_new(category_repository, test_db):
    # Test creating a new category
    category = category_repository.get_or_create(test_db, name="Comedy")
    
    # Verify the result
    assert category is not None
    assert category.name == "Comedy"

def test_category_repository_get_multiple_by_names(category_repository, test_db):
    # Create test categories
    test_category1 = Category(
        name="Action"
    )
    test_db.add(test_category1)
    
    test_category2 = Category(
        name="Drama"
    )
    test_db.add(test_category2)
    test_db.commit()
    
    # Test getting multiple categories by names
    categories = category_repository.get_multiple_by_names(
        test_db,
        names=["Action", "Drama", "Comedy"]
    )
    
    # Verify the result
    assert len(categories) == 3
    assert categories[0].name == "Action"
    assert categories[1].name == "Drama"
    assert categories[2].name == "Comedy"
