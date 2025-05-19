import os
import shutil
from datetime import datetime
from typing import List, Optional, Dict, Any
import requests
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from core.config import settings
from db.repositories.video_repository import video_repository
from db.repositories.category_repository import category_repository
from db.repositories.subtitle_repository import subtitle_repository
from models.video import Video
from schemas.video import VideoCreate, VideoUpdate, VideoSchema

class VideoService:
    """Service for video operations"""
    
    def get_video(self, db: Session, video_id: int) -> VideoSchema:
        """Get video details by ID"""
        video = video_repository.get_with_categories(db, video_id=video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        return self._map_video_to_schema(video)
    
    def list_videos(self, db: Session, skip: int = 0, limit: int = 100) -> List[VideoSchema]:
        """List all available videos with pagination"""
        videos = video_repository.get_multi(db, skip=skip, limit=limit)
        return [self._map_video_to_schema(video) for video in videos]
    
    async def upload_video(
        self,
        db: Session,
        imdb_id: str,
        file: UploadFile,
        subtitle: Optional[UploadFile] = None
    ) -> VideoSchema:
        """Upload a new video file with metadata from OMDB API"""
        # Validate file type
        content_type = file.content_type
        if not content_type.startswith("video/"):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only video files are allowed."
            )

        # Check if video with this IMDB ID already exists
        existing_video = video_repository.get_by_imdb_id(db, imdb_id=imdb_id)
        if existing_video:
            raise HTTPException(
                status_code=400,
                detail="Video with this imdb_id already exists"
            )

        # Get metadata from OMDB API
        video_metadata = self._get_omdb_metadata(imdb_id)
        
        # Create unique filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(settings.VIDEOS_DIR, filename)

        # Save video file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Prepare video data
        video_data = {
            "title": video_metadata["title"],
            "year": video_metadata["year"],
            "duration": video_metadata["duration"],
            "thumbnail": video_metadata["thumbnail"],
            "description": video_metadata["description"],
            "imdb_id": imdb_id,
            "filename": filename,
            "content_type": content_type
        }

        # Get or create categories
        categories = category_repository.get_multiple_by_names(
            db, names=video_metadata["categories"]
        )

        # Create video with categories
        db_video = video_repository.create_with_categories(
            db, obj_in=video_data, categories=categories
        )

        # Handle subtitle if provided
        if subtitle:
            await self._save_subtitle(db, db_video.id, subtitle)

        return self._map_video_to_schema(db_video)
    
    def get_video_file_path(self, db: Session, video_id: int) -> str:
        """Get the file path for a video"""
        video = video_repository.get(db, id=video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        file_path = os.path.join(settings.VIDEOS_DIR, video.filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Video file not found")
        
        return file_path
    
    def _get_omdb_metadata(self, imdb_id: str) -> Dict[str, Any]:
        """Get video metadata from OMDB API"""
        response = requests.get(
            f"https://www.omdbapi.com/?i={imdb_id}&apikey={settings.OMDB_API_KEY}"
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch metadata from OMDB API")
        
        data = response.json()
        if data.get("Error"):
            raise HTTPException(status_code=400, detail=data.get("Error"))
        
        # Extract and format metadata
        categories = data.get("Genre", "").split(",")
        categories = [category.strip() for category in categories]
        
        return {
            "title": data.get("Title"),
            "year": data.get("Year"),
            "duration": data.get("Runtime", "0 min").split(" ")[0],
            "thumbnail": data.get("Poster"),
            "description": data.get("Plot"),
            "categories": categories
        }
    
    async def _save_subtitle(self, db: Session, video_id: int, subtitle_file: UploadFile) -> None:
        """Save a subtitle file and create a database entry"""
        subtitle_path = os.path.join(settings.SUBTITLES_DIR, subtitle_file.filename)
        
        with open(subtitle_path, "wb") as buffer:
            shutil.copyfileobj(subtitle_file.file, buffer)
        
        # Create subtitle in database
        subtitle_data = {
            "video_id": video_id,
            "filename": subtitle_file.filename,
            "language": "en"  # Default language
        }
        
        subtitle_repository.create(db, obj_in=SubtitleCreate(**subtitle_data))
    
    def _map_video_to_schema(self, video: Video) -> VideoSchema:
        """Map a Video model to a VideoSchema"""
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
video_service = VideoService()
