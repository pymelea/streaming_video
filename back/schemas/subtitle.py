from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SubtitleBase(BaseModel):
    """Base schema for subtitle data"""
    language: str = "en"
    format: str = "srt"

class SubtitleCreate(SubtitleBase):
    """Schema for creating a new subtitle"""
    video_id: int
    filename: str

class SubtitleUpdate(SubtitleBase):
    """Schema for updating an existing subtitle"""
    language: Optional[str] = None
    format: Optional[str] = None

class SubtitleSchema(SubtitleBase):
    """Schema for subtitle response"""
    id: int
    video_id: int
    filename: str
    content_url: str

    class Config:
        orm_mode = True

class TranslationRequest(BaseModel):
    """Schema for translation request"""
    text: str
    source_language: str = "auto"
    target_language: str

class TranslationResponse(BaseModel):
    """Schema for translation response"""
    translated_text: str
    source_language: str
    target_language: str