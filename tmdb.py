import requests
import json
from pprint import pprint
from movie import Movie
from datetime import datetime
import locale
import isodate
import os

locale.setlocale(locale.LC_ALL, 'en_US')

class TheMoviedb:

    def __init__(self, api_key):
        self.api_key = api_key

    def tmdb_get_by_id(self, id):
        r = requests.get(f'https://api.themoviedb.org/3/movie/{id}?api_key={self.api_key}')
        r = r.json()
        if 'status_code' not in r:
            title = r['title']
            original_title = r['original_title']
            release_date = r['release_date']
            if r['adult'] == 'False':
                rating = 'TP'
            else:
                rating = '-18'
            duration = r['runtime']
            box_office = r['revenue']
            imdb_id = r['imdb_id']
            imdb_score = r['vote_average']
            synopsis = r['overview']
            production_budget = r['budget']
            popularity = r['popularity']
            awards = None
            marketing_budget = None
            tagline = r['tagline']
            if r['genres']:
                if r['genres'][0]:
                    genre_split0 = r['genres'][0]
                    genre0 = genre_split0['name']
                    if r['genres'][1]:
                        genre_split1 = r['genres'][1]
                        genre1 = genre_split1['name']
                        if r['genres'][2]:
                            genre_split2 = r['genres'][2]
                            genre2 = genre_split2['name']
                            genre = f"{genre0}, {genre1}, {genre2}"
                        else:
                            genre = f"{genre0}, {genre1}"
                    else:
                        genre = f"{genre0}"
            else:
                genre = None  
            is_3D = None

            movie = Movie(imdb_id, 
                title, 
                original_title, 
                genre, 
                synopsis, 
                tagline, 
                duration, 
                production_budget, 
                marketing_budget, 
                release_date, 
                rating, 
                imdb_score, 
                box_office,
                popularity,
                awards,
                is_3D)
            return movie
        if r['status_code'] == 34:
            movie = f"Aucun film avec l'id {id} n'existe dans TMDBapi"
            return movie

    # def omdb_gat_by_year(self, year):

# film = TheMoviedb(api_key_tmdb)
# Film = film.tmdb_get_by_id('550')
# print(Film)

