import os
from typing import Optional
from fastapi import HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from core.config import settings
from db.repositories.subtitle_repository import subtitle_repository
from models.subtitle import Subtitle

class SubtitleService:
    """Service for subtitle operations"""
    
    def get_subtitle_content(self, db: Session, subtitle_id: int) -> Response:
        """Get subtitle file content by ID"""
        # Find the subtitle in the database
        subtitle = subtitle_repository.get(db, id=subtitle_id)
        if not subtitle:
            raise HTTPException(status_code=404, detail="Subtitle not found")

        # Check if the subtitle file exists
        subtitle_path = os.path.join(settings.SUBTITLES_DIR, subtitle.filename)
        if not os.path.exists(subtitle_path):
            raise HTTPException(status_code=404, detail="Subtitle file not found")

        # Read the subtitle file
        with open(subtitle_path, "r") as f:
            subtitle_content = f.read()

        # Determine the appropriate media type based on the subtitle format
        media_type = self._get_media_type_for_subtitle(subtitle.filename)

        # Return the subtitle content with appropriate headers
        return Response(
            content=subtitle_content,
            media_type=media_type,
            headers={
                'Content-Disposition': f'attachment; filename={subtitle.filename}',
                # Allow cross-origin requests for video players
                'Access-Control-Allow-Origin': '*'
            }
        )
    
    def get_subtitles_for_video(self, db: Session, video_id: int):
        """Get all subtitles for a video"""
        return subtitle_repository.get_by_video_id(db, video_id=video_id)
    
    def _get_media_type_for_subtitle(self, filename: str) -> str:
        """Get the appropriate media type for a subtitle file"""
        # Common subtitle formats and their MIME types
        mime_types = {
            'srt': 'application/x-subrip',
            'vtt': 'text/vtt',
            'ass': 'text/x-ssa',
            'ssa': 'text/x-ssa',
            'sub': 'text/x-subviewer'
        }

        # Get the file extension from the filename
        file_ext = filename.split('.')[-1].lower() if '.' in filename else ''

        # Use the appropriate MIME type or default to text/plain
        return mime_types.get(file_ext, 'text/plain')

# Create a singleton instance
subtitle_service = SubtitleService()
