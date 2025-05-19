from typing import List, Optional
from sqlalchemy.orm import Session

from db.repositories.base import BaseRepository
from models.subtitle import Subtitle
from schemas.subtitle import SubtitleCreate, SubtitleUpdate

class SubtitleRepository(BaseRepository[Subtitle, SubtitleCreate, SubtitleUpdate]):
    """Repository for subtitle operations"""
    
    def __init__(self):
        super().__init__(Subtitle)
    
    def get_by_video_id(self, db: Session, *, video_id: int) -> List[Subtitle]:
        """Get all subtitles for a video"""
        return db.query(Subtitle).filter(Subtitle.video_id == video_id).all()
    
    def get_by_video_id_and_language(self, db: Session, *, video_id: int, language: str) -> Optional[Subtitle]:
        """Get a subtitle by video ID and language"""
        return db.query(Subtitle).filter(
            Subtitle.video_id == video_id,
            Subtitle.language == language
        ).first()

# Create a singleton instance
subtitle_repository = SubtitleRepository()
