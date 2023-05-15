import requests
import json

API_KEY = '?api_key=f830493fe21a93ae2fbc53fe087f8961'
URL_BASE = 'https://api.themoviedb.org/3/'
IMG_URL_BASE = f'https://image.tmdb.org/t/p/w500/'

class TMDB_wrapper:
    def __init__(self, api_key: str, url_base: str = 'https://api.themoviedb.org/3/', img_url_base: str = 'https://image.tmdb.org/t/p/w500/') -> None:
        self.api_key = api_key
        self.url_base = url_base
        self.img_url_base = img_url_base

    def get_url(url):
        response = requests.get(url)
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            return None

    def get_movie(self, id):
        url = f'{self.url_base}movie/{id}{self.api_key}'
        return self.get_url(url)

    def get_discover(self, page_start, page_stop):
        movies = []
        for page in range(page_start, page_stop):
            url = f'{self.url_base}discover/movie/{self.api_key}&page={page}'
            discover = self.get_url(url)
            if discover != None:
                for m in discover['results']:
                    movies.append(m['id'])

        return movies

    def get_credits(self, movie_id):
        url = f'{self.url_base}movie/{movie_id}/credits{self.api_key}'
        return self.get_url(url)
