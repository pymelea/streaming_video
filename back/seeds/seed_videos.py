import os
import sys
from datetime import datetime
from sqlalchemy.orm import Session

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models
from models.video import Video
from models.category import Category
from models.subtitle import Subtitle
from db.database import SessionLocal, engine

# Spider-Man movie data (to avoid requiring external API)
spiderman_movie_data = {
    "tt0145487": {
        "Title": "Spider-Man",
        "Year": "2002",
        "Runtime": "121 min",
        "Poster": "https://m.media-amazon.com/images/M/MV5BZDEyN2NhMjgtMjdhNi00MmNlLWE5YTgtZGE4MzNjMTRlMGEwXkEyXkFqcGdeQXVyNDUyOTg3Njg@._V1_SX300.jpg",
        "Plot": "After being bitten by a genetically-modified spider, a shy teenager gains spider-like abilities that he uses to fight injustice as a masked superhero and face a vengeful enemy.",
        "Genre": "Action, Adventure, Sci-Fi"
    },
    "tt0316654": {
        "Title": "Spider-Man 2",
        "Year": "2004",
        "Runtime": "127 min",
        "Poster": "https://m.media-amazon.com/images/M/MV5BMzY2ODk4NmUtOTVmNi00ZTdkLTlmOWYtMmE2OWVhNTU2OTVkXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg",
        "Plot": "Peter Parker is beset with troubles in his failing personal life as he battles a brilliant scientist named Doctor Otto Octavius.",
        "Genre": "Action, Adventure, Sci-Fi"
    },
    "tt0413300": {
        "Title": "Spider-Man 3",
        "Year": "2007",
        "Runtime": "139 min",
        "Poster": "https://m.media-amazon.com/images/M/MV5BYTk3MDljOWQtNGI2My00OTEzLTlhYjQtOTQ4ODM2MzUwY2IwXkEyXkFqcGdeQXVyNTIzOTk5ODM@._V1_SX300.jpg",
        "Plot": "A strange black entity from another world bonds with Peter Parker and causes inner turmoil as he contends with new villains, temptations, and revenge.",
        "Genre": "Action, Adventure, Sci-Fi"
    },
    "tt0948470": {
        "Title": "The Amazing Spider-Man",
        "Year": "2012",
        "Runtime": "136 min",
        "Poster": "https://m.media-amazon.com/images/M/MV5BMjMyOTM4MDMxNV5BMl5BanBnXkFtZTcwNjIyNzExOA@@._V1_SX300.jpg",
        "Plot": "After Peter Parker is bitten by a genetically altered spider, he gains newfound, spider-like powers and ventures out to save the city from the machinations of a mysterious reptilian foe.",
        "Genre": "Action, Adventure, Fantasy"
    },
    "tt2250912": {
        "Title": "The Amazing Spider-Man 2",
        "Year": "2014",
        "Runtime": "142 min",
        "Poster": "https://m.media-amazon.com/images/M/MV5BOTA5NDYxNTg0OV5BMl5BanBnXkFtZTgwODE5NzU1MTE@._V1_SX300.jpg",
        "Plot": "When New York is put under siege by Oscorp, it is up to Spider-Man to save the city he swore to protect as well as his loved ones.",
        "Genre": "Action, Adventure, Sci-Fi"
    },
    "tt4633694": {
        "Title": "Spider-Man: Homecoming",
        "Year": "2017",
        "Runtime": "133 min",
        "Poster": "https://m.media-amazon.com/images/M/MV5BNTk4ODQ1MzgzNl5BMl5BanBnXkFtZTgwMTMyMzM4MTI@._V1_SX300.jpg",
        "Plot": "Peter Parker balances his life as an ordinary high school student in Queens with his superhero alter-ego Spider-Man, and finds himself on the trail of a new menace prowling the skies of New York City.",
        "Genre": "Action, Adventure, Sci-Fi"
    },
    "tt6320628": {
        "Title": "Spider-Man: Far from Home",
        "Year": "2019",
        "Runtime": "129 min",
        "Poster": "https://m.media-amazon.com/images/M/MV5BMGZlNTY1ZWUtYTMzNC00ZjUyLWE0MjQtMTMxN2E3ODYxMWVmXkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_SX300.jpg",
        "Plot": "Following the events of Avengers: Endgame, Spider-Man must step up to take on new threats in a world that has changed forever.",
        "Genre": "Action, Adventure, Sci-Fi"
    },
    "tt10872600": {
        "Title": "Spider-Man: No Way Home",
        "Year": "2021",
        "Runtime": "148 min",
        "Poster": "https://m.media-amazon.com/images/M/MV5BZWMyYzFjYTYtNTRjYi00OGExLWE2YzgtOGRmYjAxZTU3NzBiXkEyXkFqcGdeQXVyMzQ0MzA0NTM@._V1_SX300.jpg",
        "Plot": "With Spider-Man's identity now revealed, Peter asks Doctor Strange for help. When a spell goes wrong, dangerous foes from other worlds start to appear, forcing Peter to discover what it truly means to be Spider-Man.",
        "Genre": "Action, Adventure, Fantasy"
    },
    "tt9362722": {
        "Title": "Spider-Man: Across the Spider-Verse",
        "Year": "2023",
        "Runtime": "140 min",
        "Poster": "https://m.media-amazon.com/images/M/MV5BMzI0NmVkMjEtYmY4MS00ZDMxLTlkZmEtMzU4MDQxYTMzMjU2XkEyXkFqcGdeQXVyMzQ0MzA0NTM@._V1_SX300.jpg",
        "Plot": "Miles Morales catapults across the Multiverse, where he encounters a team of Spider-People charged with protecting its very existence. When the heroes clash on how to handle a new threat, Miles must redefine what it means to be a hero.",
        "Genre": "Animation, Action, Adventure"
    },
    "tt5029376": {
        "Title": "Spider-Man: Into the Spider-Verse",
        "Year": "2018",
        "Runtime": "117 min",
        "Poster": "https://m.media-amazon.com/images/M/MV5BMjMwNDkxMTgzOF5BMl5BanBnXkFtZTgwNTkwNTQ3NjM@._V1_SX300.jpg",
        "Plot": "Teen Miles Morales becomes the Spider-Man of his universe, and must join with five spider-powered individuals from other dimensions to stop a threat for all realities.",
        "Genre": "Animation, Action, Adventure"
    }
}

# List of Spider-Man movie IMDb IDs
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


def seed_spiderman_movies():
    """Seed the database with Spider-Man movies"""
    # Ensure necessary directories exist
    os.makedirs("uploads/videos", exist_ok=True)
    os.makedirs("uploads/subtitles", exist_ok=True)

    # Create test subtitle file if it doesn't exist
    subtitle_path = "uploads/subtitles/test.srt"
    if not os.path.exists(subtitle_path):
        subtitle_content = """1
00:00:01,000 --> 00:00:04,000
Hello, welcome to this Spider-Man movie.

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

    db = SessionLocal()
    try:
        print("Starting to seed Spider-Man movies...")

        for imdb_id in spiderman_movies:
            # Check if movie already exists
            existing_movie = db.query(Video).filter(
                Video.imdb_id == imdb_id).first()
            if existing_movie:
                print(
                    f"Movie with IMDb ID {imdb_id} already exists. Skipping...")
                continue

            # Get movie data from our predefined dictionary
            if imdb_id not in spiderman_movie_data:
                print(f"No data found for IMDb ID {imdb_id}. Skipping...")
                continue
                
            movie_data = spiderman_movie_data[imdb_id]
            
            # Extract movie data
            title = movie_data["Title"]
            # Handle TV series years like "2019-2023"
            year = movie_data["Year"].split('-')[0]
            try:
                duration = int(movie_data["Runtime"].split(
                    " ")[0]) if movie_data["Runtime"] != "N/A" else 0
            except:
                duration = 0
            thumbnail = movie_data["Poster"]
            description = movie_data["Plot"]

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

            # Add subtitle for the video
            subtitle_filename = "test.srt"

            # Check if subtitle already exists for this video
            existing_subtitle = db.query(Subtitle).filter(
                Subtitle.video_id == db_video.id).first()
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
            categories = movie_data["Genre"].split(",")
            categories = [category.strip() for category in categories]

            for category_name in categories:
                # Check if category exists
                db_category = db.query(Category).filter(
                    Category.name == category_name).first()
                if not db_category:
                    # Create new category
                    db_category = Category(name=category_name)
                    db.add(db_category)
                    db.commit()
                    db.refresh(db_category)

                # Add category to video
                db_video.categories.append(db_category)

            db.commit()
            print(f"Added movie: {title} ({year})")

        print("Finished seeding Spider-Man movies!")
    except Exception as e:
        print(f"Error seeding movies: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_spiderman_movies()
