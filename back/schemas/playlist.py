from pydantic import BaseModel
from typing import Optional, List
from schemas.video import VideoSchema


class PlaylistBase(BaseModel):
    """Base schema for playlist data"""
    name: str
    description: Optional[str] = None
    videos: Optional[List[VideoSchema]] = None


class PlaylistCreate(PlaylistBase):
    """Schema for creating a new playlist"""
    pass


class PlaylistUpdate(PlaylistBase):
    """Schema for updating an existing playlist"""
    name: Optional[str] = None
    description: Optional[str] = None
    videos: Optional[List[VideoSchema]] = None


class PlaylistSchema(PlaylistBase):
    """Schema for playlist response"""
    id: int

    class Config:
        orm_mode = True
