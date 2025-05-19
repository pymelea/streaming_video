from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_db
from services.subtitle_service import subtitle_service

router = APIRouter()

@router.get("/content/{subtitle_id}")
async def get_subtitle_content(subtitle_id: int, db: Session = Depends(get_db)):
    """
    Get subtitle file content by ID
    """
    return subtitle_service.get_subtitle_content(db, subtitle_id=subtitle_id)
