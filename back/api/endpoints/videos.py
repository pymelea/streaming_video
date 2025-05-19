from typing import List, Optional
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from api.dependencies import get_db
from services.video_service import video_service
from schemas.video import VideoSchema, VideoCreate
from utils.file_handlers import get_range_header, ranged_file_sender, file_sender
import os

router = APIRouter(
    tags=["Videos"],
)


@router.get("/", response_model=List[VideoSchema])
def list_videos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all available videos with pagination
    """
    return video_service.list_videos(db, skip=skip, limit=limit)


@router.get("/{video_id}", response_model=VideoSchema)
def get_video(video_id: int, db: Session = Depends(get_db)):
    """
    Get video details by ID
    """
    return video_service.get_video(db, video_id=video_id)


@router.post("/upload", status_code=status.HTTP_201_CREATED, response_model=VideoSchema)
async def upload_video(
    imdb_id: str,
    file: UploadFile = File(...),
    subtitle: Optional[UploadFile] = None,
    db: Session = Depends(get_db)
):
    """
    Upload a new video file with metadata and imdb_id to get video metadata from OMDB API
    """
    return await video_service.upload_video(db, imdb_id=imdb_id, file=file, subtitle=subtitle)


@router.get("/stream/{video_id}")
async def stream_video(video_id: int, request: Request, db: Session = Depends(get_db)):
    """
    Stream video with support for range requests (important for seeking in videos)
    """
    file_path = video_service.get_video_file_path(db, video_id=video_id)

    # Get video details for content type
    video = video_service.get_video(db, video_id=video_id)
    file_size = os.path.getsize(file_path)
    content_type = "video/mp4"  # Default content type

    # Handle range requests
    range_header = request.headers.get("range")

    if range_header:
        start, end = get_range_header(range_header, file_size)
        size = end - start + 1

        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(size),
            "Content-Disposition": f"inline; filename={video['filename']}"
        }

        return StreamingResponse(
            ranged_file_sender(file_path, start, end),
            status_code=206,
            media_type=content_type,
            headers=headers
        )

    # No range header, return full file
    return StreamingResponse(
        file_sender(file_path),
        media_type=content_type,
        headers={
            "Accept-Ranges": "bytes",
            "Content-Length": str(file_size),
            "Content-Disposition": f"inline; filename={video['filename']}"
        }
    )
