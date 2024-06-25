from modules.logging import setup_logging
from modules.config import load_configurations
from medicure import Medicure, DubbingSupplier
from tmdbv3api import TMDb, Movie
from pathlib import Path
import os

# Load configurations and setup logging
config = load_configurations()
logging = setup_logging()

TMDB_API = config["TMDB"]["API_KEY"]
TMDB_CONTENT = config["TMDB"]["CONTENT"]

class MOVIE_TRACKS:
    def __init__(self):
        self.movie = Movie()
        
class TMDB:
    def __init__(self):
        self.tmdb_api = TMDb()
        self.tmdb_api.language = "en"
        self.tmdb_api.debug = True
        self.tmdb_api.api_key = TMDB_API
        self.tvshows_directory = Path(TMDB_CONTENT)
        self.medicure = Medicure(tmdb_api_key=TMDB_API, tvshows_directory=self.tvshows_directory)
    
    def process_media(self, title, imdb_id, season_number, file_search_patterns, video_lang_code, video_source, video_format, dubbing_suppliers):
        # Ensure the directory for the season is created
        season_directory = self.tvshows_directory / title / f"Series {season_number}"
        try:
            season_directory.mkdir(parents=True, exist_ok=True)
            logging.info(f"Directory {season_directory} created or already exists.")
        except Exception as e:
            logging.error(f"Failed to create directory {season_directory}: {e}")
            return  # Stop further execution if directory creation fails

        logging.info(f"Starting to process media for title: {title}")
        try:
            # Assuming Medicure uses its initialized tvshows_directory internally
            self.medicure.treat_media(
                imdb_id=imdb_id,
                file_search_patterns=file_search_patterns,
                video_language_code=video_lang_code,
                video_source=video_source,
                video_release_format=video_format,
                dubbing_suppliers=dubbing_suppliers,
                season_number=season_number,
            )
            logging.info(f"Media processing successful for {title}, IMDb ID: {imdb_id}")
        except Exception as e:
            logging.error(f"Failed to process media for {title}, IMDb ID: {imdb_id}, Error: {e}")
            
def process_media_with_tmdb(title):
    # Initialize TMDB instance
    tmdb_instance = TMDB()

    # Setup media processing details
    imdb_id = title  # Using title as IMDb ID placeholder
    season_number = 6
    file_search_patterns = ["*.mp4", "*.mkv", "PSA"]
    video_lang_code = "eng"
    video_source = "PSA"
    video_format = "WEB-DL"
    dubbing_suppliers = [
        DubbingSupplier(name='original', file_id=0, correct_language_code='eng', audio_language_code='eng', subtitle_language_code='eng')
    ]

    # Call the process_media method
    tmdb_instance.process_media(
        title, 
        imdb_id, 
        season_number, 
        file_search_patterns, 
        video_lang_code, 
        video_source, 
        video_format, 
        dubbing_suppliers
    )
