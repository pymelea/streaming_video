from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from db.database import Base
from models.associations import video_category, playlist_video


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    imdb_id = Column(String)
    filename = Column(String)
    upload_date = Column(DateTime, default=datetime.now())
    categories = relationship(
        "Category", secondary=video_category, back_populates="videos")
    playlists = relationship(
        "Playlist", secondary=playlist_video, back_populates="videos", lazy="joined")
    title = Column(String)
    description = Column(String)
    duration = Column(Integer)
    thumbnail = Column(String)
    year = Column(Integer)
    subtitles = relationship("Subtitle", back_populates="video")
    content_type = Column(String)
