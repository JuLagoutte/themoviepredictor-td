import requests
import json
from pprint import pprint
from movie import Movie
from datetime import datetime
import locale
import isodate
import os

locale.setlocale(locale.LC_ALL, 'en_US')


# with open('omdbapikey.txt', 'r') as file:
#     api_key = file.read()

class Omdb:

    def __init__(self, api_key):
        self.api_key = api_key

    def omdb_get_by_id(self, id):
        r = requests.get(f'http://www.omdbapi.com/?i={id}&apikey={self.api_key}')
        r = r.json()
        if r['Response'] == "False":
            movie = f"Aucun film avec l'id {id} n'existe dans OMDBapi"
            return movie
        else:
            imdb_id_str = r['imdbID']
            imdb_id = imdb_id_str.replace("tt", "")
            title = r['Title']
            original_title = r['Title']
            release_date_class = r['Released']
            release_date_strip = release_date_class.strip()
            release_date_object = datetime.strptime(release_date_strip, '%d %b %Y')
            release_date = release_date_object.strftime('%Y-%m-%d')
            if r['Rated'] == 'R':
                rating = '-12'
            elif r['Rated'] == 'NC-17':
                rating = '-16'
            else:
                rating = 'TP'
            duration = r['Runtime']
            duration = duration.split()
            duration = duration[0]
            if r['Type']=="movie":
                box_office = r['BoxOffice']
                if r['BoxOffice'] == 'N/A':
                    box_office = None
            else:
                box_office = None
            imdb_score = r['imdbRating']
            popularity = r['imdbVotes']
            synopsis = r['Plot']
            production_budget = None
            marketing_budget = None
            tagline = None
            awards = r['Awards']
            genre = r['Genre']
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

    # def omdb_gat_by_year(self, year):
        
    
# film = Omdb(api_key)
# Film = film.omdb_get_by_id('tt7286456', api_key)
# print(Film.imdb_id)




# class Get_movie:
#     def __init__(self, url, id):
#         self.url = url
#         # self.id = id
