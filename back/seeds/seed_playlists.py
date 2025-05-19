from db.repositories.video_repository import video_repository
from db.repositories.playlist_repository import playlist_repository
from db.database import SessionLocal
from models.playlist import Playlist
from models.video import Video
import os
import sys
from sqlalchemy.orm import Session

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models and repositories

# Spider-Man movie IMDb IDs (same as in seed_videos.py)
spiderman_movies = [
    "tt0145487",  # Spider-Man (2002)
    "tt0316654",  # Spider-Man 2 (2004)
    "tt0413300",  # Spider-Man 3 (2007)
    "tt0948470",  # The Amazing Spider-Man (2012)
    "tt2250912",  # The Amazing Spider-Man 2 (2014)
    "tt4633694",  # Spider-Man: Homecoming (2017)
    "tt6320628",  # Spider-Man: Far from Home (2019)
    "tt10872600",  # Spider-Man: No Way Home (2021)
    "tt9362722",  # Spider-Man: Across the Spider-Verse (2023)
    "tt5029376",  # Spider-Man: Into the Spider-Verse (2018)
]


def seed_spiderman_playlist():
    """Create a Spider-Man playlist containing all Spider-Man movies"""
    db = SessionLocal()
    try:
        print("Creating Spider-Man playlist...")

        # Check if playlist already exists
        existing_playlist = playlist_repository.get_by_name(
            db, name="Spider-Man Collection")
        if existing_playlist:
            print("Spider-Man playlist already exists. Clearing videos...")
            existing_playlist.videos = []
            db.commit()
            db.refresh(existing_playlist)
            playlist = existing_playlist
        else:
            # Create new playlist
            playlist = Playlist(
                name="Spider-Man Collection",
                description="Complete collection of Spider-Man movies, including the original trilogy, The Amazing Spider-Man, MCU and Spider-Verse."
            )
            db.add(playlist)
            db.commit()
            db.refresh(playlist)
            print("Created new Spider-Man playlist")

        # Add Spider-Man movies to playlist
        videos_added = 0
        for imdb_id in spiderman_movies:
            # Get video by IMDb ID
            video = video_repository.get_by_imdb_id(db, imdb_id=imdb_id)
            if not video:
                print(f"Video with IMDb ID {imdb_id} not found. Skipping...")
                continue

            # Add video to playlist
            playlist.videos.append(video)
            videos_added += 1
            print(f"Added {video.title} ({video.year}) to Spider-Man playlist")

        db.commit()
        print(
            f"Successfully added {videos_added} videos to Spider-Man playlist")

        # Print playlist details
        print(f"\nPlaylist: {playlist.name}")
        print(f"Description: {playlist.description}")
        print(f"Total videos: {len(playlist.videos)}")
        print("Videos:")
        for video in playlist.videos:
            print(f"- {video.title} ({video.year})")

    except Exception as e:
        print(f"Error creating Spider-Man playlist: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_spiderman_playlist()
