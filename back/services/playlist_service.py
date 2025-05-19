from typing import List, Dict, Any
from sqlalchemy.orm import Session

from db.repositories.playlist_repository import playlist_repository
from db.repositories.video_repository import video_repository
from models.playlist import Playlist
from models.video import Video
from core.config import settings
from schemas.playlist import PlaylistCreate, PlaylistUpdate

class PlaylistService:
    """Service for playlist operations"""
    
    def get_playlist(self, db: Session, playlist_id: int) -> Dict[str, Any]:
        """Get playlist details by ID"""
        playlist = playlist_repository.get(db, id=playlist_id)
        if not playlist:
            return None
        
        return self._map_playlist_to_schema(playlist)
        
    def get_playlist_videos(self, db: Session, playlist_id: int) -> List[Dict[str, Any]]:
        """Get videos from a specific playlist"""
        playlist = playlist_repository.get(db, id=playlist_id)
        if not playlist:
            return None
            
        return [self._map_video_to_schema(video) for video in playlist.videos] if playlist.videos else []
    
    def list_playlists(self, db: Session, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """List all playlists with pagination"""
        playlists = playlist_repository.get_multi(db, skip=skip, limit=limit)
        return [self._map_playlist_to_schema(playlist) for playlist in playlists]
    
    def create_playlist(self, db: Session, obj_in: PlaylistCreate) -> Dict[str, Any]:
        """Create a new playlist"""
        playlist = playlist_repository.create(db, obj_in=obj_in)
        return self._map_playlist_to_schema(playlist)
    
    def update_playlist(self, db: Session, db_obj: Playlist, obj_in: PlaylistUpdate) -> Dict[str, Any]:
        """Update a playlist"""
        playlist = playlist_repository.update(db, db_obj=db_obj, obj_in=obj_in)
        return self._map_playlist_to_schema(playlist)
    
    def _map_playlist_to_schema(self, playlist: Playlist) -> Dict[str, Any]:
        """Map a Playlist model to a schema dictionary"""
        return {
            "id": playlist.id,
            "name": playlist.name,
            "description": playlist.description,
            "videos": [self._map_video_to_schema(video) for video in playlist.videos] if playlist.videos else []
        }
    
    def _map_video_to_schema(self, video: Video) -> Dict[str, Any]:
        """Map a Video model to a schema dictionary"""
        return {
            "id": video.id,
            "title": video.title,
            "upload_date": video.upload_date,
            "categories": [category.name for category in video.categories],
            "imdb_id": video.imdb_id,
            "filename": video.filename,
            "stream_url": f"/videos/stream/{video.id}",
            "year": video.year,
            "duration": video.duration,
            "thumbnail": video.thumbnail,
            "description": video.description,
            "subtitles_urls": [f"/subtitles/content/{s.id}" for s in video.subtitles] if video.subtitles else [],
        }

# Create a singleton instance
playlist_service = PlaylistService()
