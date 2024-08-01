import requests
from bs4 import BeautifulSoup
import json

class NetflixError(Exception):
    pass

class NetflixItemTypeError(NetflixError):
    """Netflix ID is not valid for object."""

class NetflixItem:
    def __init__(self, netflix_id, expected_type, fetch_instantly=True):
        self.netflix_id = netflix_id
        self.expected_type = expected_type
        self.name = None
        self.description = None
        self.genre = None
        self.image_url = None
        self.metadata = None
        self.is_fetched = False

        if fetch_instantly:
            self.fetch()

    def fetch(self):
        try:
            url = f"https://www.netflix.com/it-it/title/{self.netflix_id}"
            response = requests.get(url)
            print(response.text)
            soup = BeautifulSoup(response.content, "html.parser")
            metadata_script_tag = soup.find("script", type="application/ld+json")
            metadata = json.loads(metadata_script_tag.string)
            print(metadata)
            if metadata["@type"] != self.expected_type:
                raise NetflixItemTypeError()

            self.name = metadata.get("name")
            self.description = metadata.get("description")
            self.genre = metadata.get("genre")
            self.image_url = metadata.get("image")
            self.metadata = metadata
            self.is_fetched = True

        except Exception as e:
            raise NetflixError(f"Error fetching data: {e}")

class Movie(NetflixItem):
    def __init__(self, netflix_id, fetch_instantly=True):
        super().__init__(netflix_id, "Movie", fetch_instantly)

class TVShow(NetflixItem):
    def __init__(self, netflix_id, fetch_instantly=True):
        super().__init__(netflix_id, "TVSeries", fetch_instantly)