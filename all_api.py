import requests
import json
import locale
import isodate
import os
import random

from pprint import pprint
from movie import Movie
from datetime import datetime
from omdb import Omdb
from tmdb import TheMoviedb


locale.setlocale(locale.LC_ALL, 'en_US')

class All_api :

    def __init__(self, api_key_tmdb, api_key_omdb):
        self.api_key_tmdb = api_key_tmdb
        self.api_key_omdb = api_key_omdb

    def get_by_id_imdb(self, id):
        r_tmdb = requests.get(f'https://api.themoviedb.org/3/movie/{id}?api_key={self.api_key_tmdb}')
        r_tmdb = r_tmdb.json()
        r_omdb = requests.get(f'http://www.omdbapi.com/?i={id}&apikey={self.api_key_omdb}')
        r_omdb = r_omdb.json()

        if 'status_code' not in r_tmdb and r_omdb['Response'] == "True":
            imdb_id = r_tmdb['imdb_id']
            imdb_id = imdb_id.replace("tt", "")
            imdb_id = int(imdb_id)
            title = r_tmdb['title']
            original_title = r_tmdb['original_title']
            genre = r_omdb['Genre']
            synopsis = r_tmdb['overview']
            tagline = r_tmdb['tagline']
            production_budget = r_tmdb['budget']
            marketing_budget = None
            release_date = r_tmdb['release_date']
            duration = r_tmdb['runtime']
            if r_tmdb['revenue'] == r_omdb['BoxOffice']:
                box_office = r_omdb['BoxOffice']
            else:
                box_office = r_tmdb['revenue']
            if r_omdb['Rated'] == 'R':
                rating = '-12'
            elif r_omdb['Rated'] == 'NC-17':
                rating = '-16'
            else:
                rating = 'TP'
            imdb_score = r_omdb['imdbRating']
            if r_tmdb['popularity'] != 'N/A':
                popularity = r_tmdb['popularity']
            else:
                popularity = r_omdb['imdbVotes']
            awards = r_omdb['Awards']
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
        
        elif r_tmdb['status_code'] == 34 and r_omdb['Response'] == "True":
            movie = Omdb.omdb_get_by_id(id)
            # utiliser class Omdb

        elif 'status_code' not in r_tmdb and r_omdb['Response'] == "False":
            movie = TheMoviedb.tmdb_get_by_id(id)
            # utiliser class TheMoviedb

        else:
            movie = f"Aucun film avec l'id {id} n'existe dans les Api Omdb et Tmdb"
            return movie
    
    # def get_film (self, id):