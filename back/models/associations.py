from sqlalchemy import Column, Integer, ForeignKey, Table
from db.database import Base

# Association table for many-to-many relationship between videos and categories
video_category = Table(
    'video_category',
    Base.metadata,
    Column('video_id', Integer, ForeignKey('videos.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

# Association table for many-to-many relationship between videos and playlists
playlist_video = Table(
    'playlist_video',
    Base.metadata,
    Column('playlist_id', Integer, ForeignKey('playlists.id'), primary_key=True),
    Column('video_id', Integer, ForeignKey('videos.id'), primary_key=True)
)
