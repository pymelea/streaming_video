from typing import List, Optional
from sqlalchemy.orm import Session

from db.repositories.base import BaseRepository
from models.playlist import Playlist
from schemas.playlist import PlaylistCreate, PlaylistUpdate


class PlaylistRepository(BaseRepository[Playlist, PlaylistCreate, PlaylistUpdate]):
    """Repository for playlist operations"""

    def __init__(self):
        super().__init__(Playlist)

    def get_by_name(self, db: Session, *, name: str) -> Optional[Playlist]:
        """Get a playlist by name"""
        return db.query(Playlist).filter(Playlist.name == name).first()

    def get_or_create(self, db: Session, *, name: str) -> Playlist:
        """Get a playlist by name or create it if it doesn't exist"""
        db_obj = self.get_by_name(db, name=name)
        if db_obj:
            return db_obj

        # Create new playlist
        db_obj = Playlist(name=name)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multiple_by_names(self, db: Session, *, names: List[str]) -> List[Playlist]:
        """Get multiple playlists by names, creating any that don't exist"""
        result = []
        for name in names:
            playlist = self.get_or_create(db, name=name)
            result.append(playlist)
        return result


# Create a singleton instance
playlist_repository = PlaylistRepository()
