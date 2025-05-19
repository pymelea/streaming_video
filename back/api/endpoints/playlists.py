from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_db
from db.repositories.playlist_repository import playlist_repository
from services.playlist_service import playlist_service
from schemas.playlist import PlaylistSchema, PlaylistCreate, PlaylistUpdate
from schemas.video import VideoSchema

router = APIRouter()


@router.get("/", response_model=List[PlaylistSchema])
def list_playlists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all playlists with pagination
    """
    return playlist_service.list_playlists(db, skip=skip, limit=limit)


@router.get("/{playlist_id}", response_model=PlaylistSchema)
def get_playlist(playlist_id: int, db: Session = Depends(get_db)):
    """
    Get a playlist by ID
    """
    playlist = playlist_service.get_playlist(db, playlist_id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist


@router.get("/{playlist_id}/videos", response_model=List[VideoSchema])
def get_playlist_videos(playlist_id: int, db: Session = Depends(get_db)):
    """
    Get all videos from a specific playlist
    """
    videos = playlist_service.get_playlist_videos(db, playlist_id=playlist_id)
    if videos is None:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return videos


@router.post("/", response_model=PlaylistSchema)
def create_playlist(playlist_in: PlaylistCreate, db: Session = Depends(get_db)):
    """
    Create a new playlist
    """
    # Check if playlist with this name already exists
    existing_playlist = playlist_repository.get_by_name(
        db, name=playlist_in.name)
    if existing_playlist:
        return playlist_service.get_playlist(db, playlist_id=existing_playlist.id)

    return playlist_service.create_playlist(db, obj_in=playlist_in)


@router.put("/{playlist_id}", response_model=PlaylistSchema)
def update_playlist(playlist_id: int, playlist_in: PlaylistUpdate, db: Session = Depends(get_db)):
    """
    Update a playlist
    """
    playlist = playlist_repository.get(db, id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    return playlist_service.update_playlist(db, db_obj=playlist, obj_in=playlist_in)


@router.delete("/{playlist_id}", response_model=PlaylistSchema)
def delete_playlist(playlist_id: int, db: Session = Depends(get_db)):
    """
    Delete a playlist
    """
    playlist = playlist_service.get_playlist(db, playlist_id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    result = playlist_repository.remove(db, id=playlist_id)
    return result
