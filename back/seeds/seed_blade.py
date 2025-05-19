import os
import sys
import requests
from datetime import datetime
from sqlalchemy.orm import Session

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models
from models.video import Video
from models.category import Category
from models.subtitle import Subtitle
from models.playlist import Playlist
from db.database import SessionLocal, engine
from core.config import settings

# Function to get movie data from OMDB API
def get_movie_data_from_omdb(imdb_id):
    """Get movie data from OMDB API"""
    try:
        response = requests.get(
            f"https://www.omdbapi.com/?i={imdb_id}&apikey={settings.OMDB_API_KEY}"
        )
        
        if response.status_code != 200:
            print(f"Failed to fetch data for {imdb_id}. Status code: {response.status_code}")
            return None
        
        data = response.json()
        if data.get("Error"):
            print(f"Error fetching data for {imdb_id}: {data.get('Error')}")
            return None
            
        return data
    except Exception as e:
        print(f"Exception fetching data for {imdb_id}: {str(e)}")
        return None

# List of Blade movie IMDb IDs
blade_movies = [
    "tt0120611",  # Blade (1998)
    "tt0187738",  # Blade II (2002)
    "tt0359013",  # Blade: Trinity (2004)
    "tt10671440"  # Blade (upcoming, may not have complete data yet)
]


def seed_blade_collection():
    """Seed the database with Blade movies and create a playlist"""
    # Ensure necessary directories exist
    os.makedirs("uploads/videos", exist_ok=True)
    os.makedirs("uploads/subtitles", exist_ok=True)

    # Create test subtitle file if it doesn't exist
    subtitle_path = "uploads/subtitles/test.srt"
    if not os.path.exists(subtitle_path):
        subtitle_content = """1
00:00:01,000 --> 00:00:04,000
Hello, welcome to this Blade movie.

2
00:00:05,000 --> 00:00:09,000
This is a sample subtitle file for testing purposes.

3
00:00:10,000 --> 00:00:15,000
Enjoy the movie!
"""
        with open(subtitle_path, "w") as f:
            f.write(subtitle_content)
        print("Created test subtitle file")

    # Create test video file if it doesn't exist
    video_path = "uploads/videos/test.mp4"
    if not os.path.exists(video_path):
        # Create an empty file
        with open(video_path, "w") as f:
            f.write("")
        print("Created test video file")

    db = SessionLocal()
    try:
        print("Starting to seed Blade collection...")
        
        # Dictionary to store created videos
        created_videos = {}
        
        # 1. Create the videos
        for imdb_id in blade_movies:
            # Check if movie already exists
            existing_movie = db.query(Video).filter(Video.imdb_id == imdb_id).first()
            if existing_movie:
                print(f"Movie with IMDb ID {imdb_id} already exists. Using existing movie.")
                created_videos[imdb_id] = existing_movie
                continue

            # Get movie data from OMDB API
            movie_data = get_movie_data_from_omdb(imdb_id)
            if not movie_data:
                print(f"No data found for IMDb ID {imdb_id}. Skipping...")
                continue
            
            # Extract movie data
            title = movie_data.get("Title", "Unknown Title")
            # Handle TV series years like "2019-2023"
            year = movie_data.get("Year", "2000").split('-')[0]
            try:
                runtime = movie_data.get("Runtime", "0 min")
                duration = int(runtime.split(" ")[0]) if runtime != "N/A" else 0
            except:
                duration = 0
            thumbnail = movie_data.get("Poster", "")
            description = movie_data.get("Plot", "")

            # Use the existing test.mp4 file for all movies
            filename = "test.mp4"

            # Create the video entry
            db_video = Video(
                title=title,
                year=year,
                duration=duration,
                thumbnail=thumbnail,
                description=description,
                imdb_id=imdb_id,
                filename=filename,
                content_type="video/mp4"
            )
            db.add(db_video)
            db.commit()
            db.refresh(db_video)
            
            # Store the created video
            created_videos[imdb_id] = db_video

            # Add subtitle for the video
            subtitle_filename = "test.srt"

            # Check if subtitle already exists for this video
            existing_subtitle = db.query(Subtitle).filter(Subtitle.video_id == db_video.id).first()
            if not existing_subtitle:
                # Create subtitle entry
                db_subtitle = Subtitle(
                    video_id=db_video.id,
                    filename=subtitle_filename,
                    language="en"
                )
                db.add(db_subtitle)
                db.commit()
                db.refresh(db_subtitle)
                print(f"Added subtitle for {title}")

            # Get categories and add them to the video
            genre = movie_data.get("Genre", "")
            categories = genre.split(",") if genre else []
            categories = [category.strip() for category in categories if category.strip()]

            for category_name in categories:
                # Check if category exists
                db_category = db.query(Category).filter(Category.name == category_name).first()
                if not db_category:
                    # Create new category
                    db_category = Category(name=category_name)
                    db.add(db_category)
                    db.commit()
                    db.refresh(db_category)

                # Add category to video
                if db_category not in db_video.categories:
                    db_video.categories.append(db_category)

            db.commit()
            print(f"Added movie: {title} ({year})")
        
        # 2. Create the Blade playlist
        print("\nCreating Blade playlist...")
        
        # Check if playlist already exists
        existing_playlist = db.query(Playlist).filter(Playlist.name == "Blade Collection").first()
        if existing_playlist:
            print("Blade playlist already exists. Clearing videos...")
            existing_playlist.videos = []
            db.commit()
            db.refresh(existing_playlist)
            playlist = existing_playlist
        else:
            # Create new playlist
            playlist = Playlist(
                name="Blade Collection",
                description="Complete collection of Blade movies, featuring the iconic vampire hunter."
            )
            db.add(playlist)
            db.commit()
            db.refresh(playlist)
            print("Created new Blade playlist")
        
        # Add Blade movies to playlist
        videos_added = 0
        for imdb_id in blade_movies:
            if imdb_id in created_videos:
                video = created_videos[imdb_id]
                # Add video to playlist
                playlist.videos.append(video)
                videos_added += 1
                print(f"Added {video.title} ({video.year}) to Blade playlist")
        
        db.commit()
        print(f"Successfully added {videos_added} videos to Blade playlist")
        
        # Print playlist details
        print(f"\nPlaylist: {playlist.name}")
        print(f"Description: {playlist.description}")
        print(f"Total videos: {len(playlist.videos)}")
        print("Videos:")
        for video in playlist.videos:
            print(f"- {video.title} ({video.year})")
            
        print("\nFinished seeding Blade collection!")
    except Exception as e:
        print(f"Error seeding Blade collection: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    seed_blade_collection()
