from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Video schemas
class VideoBase(BaseModel):
    """Base schema for video data"""
    title: str
    description: Optional[str] = None
    year: Optional[int] = None
    duration: Optional[int] = None
    thumbnail: Optional[str] = None
    imdb_id: Optional[str] = None


class VideoCreate(VideoBase):
    """Schema for creating a new video"""
    filename: str
    content_type: str


class VideoUpdate(VideoBase):
    """Schema for updating an existing video"""
    title: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None
    duration: Optional[int] = None
    thumbnail: Optional[str] = None


class VideoSchema(VideoBase):
    """Schema for video response"""
    id: int
    filename: str
    upload_date: datetime
    categories: List[str] = []
    stream_url: str
    subtitles_urls: List[str] = []

    class Config:
        orm_mode = True
