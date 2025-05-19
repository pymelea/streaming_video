from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from db.repositories.base import BaseRepository
from models.video import Video
from schemas.video import VideoCreate, VideoUpdate

class VideoRepository(BaseRepository[Video, VideoCreate, VideoUpdate]):
    """Repository for video operations"""
    
    def __init__(self):
        super().__init__(Video)
    
    def get_by_imdb_id(self, db: Session, *, imdb_id: str) -> Optional[Video]:
        """Get a video by IMDB ID"""
        return db.query(Video).filter(Video.imdb_id == imdb_id).first()
    
    def get_with_categories(self, db: Session, *, video_id: int) -> Optional[Video]:
        """Get a video with its categories"""
        return db.query(Video).filter(Video.id == video_id).first()
    
    def get_with_subtitles(self, db: Session, *, video_id: int) -> Optional[Video]:
        """Get a video with its subtitles"""
        return db.query(Video).filter(Video.id == video_id).first()
    
    def create_with_categories(self, db: Session, *, obj_in: Dict[str, Any], categories: List) -> Video:
        """Create a video with categories"""
        db_obj = Video(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Add categories to video
        for category in categories:
            db_obj.categories.append(category)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

# Create a singleton instance
video_repository = VideoRepository()
