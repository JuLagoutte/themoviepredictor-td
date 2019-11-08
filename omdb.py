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
#     apikey = file.read()

apikey = os.environ['OMDB_API_KEY']

class Omdb:

    def omdb_get_by_id(self, id):
        r = requests.get(f'http://www.omdbapi.com/?i={id}&apikey={apikey}')
        r = r.json()
        if r['Response'] == "False":
            movie = print(f"Aucun film avec l'id {id} n'existe dans OMDBapi")
            return movie
        else:
            title = r['Title']
            original_title = r['Title']
            release_date_class = r['Released']
            release_date_strip = release_date_class.strip()
            release_date_object = datetime.strptime(release_date_strip, '%d %b %Y')
            release_date = release_date_object.strftime('%Y-%m-%d')
            # rating = "None"
            duration = r['Runtime']
            duration = duration.split()
            duration = duration[0]
            if r['Type']=="movie":
                box_office = r['BoxOffice']
                if r['BoxOffice'] == 'N/A':
                    box_office = None
            else:
                box_office = None
            omdb_id = r['imdbID']
            omdb_id = omdb_id.replace("tt", "")
            imdb_score = r['imdbRating']

            movie = Movie(omdb_id, title, original_title, duration, release_date, imdb_score, box_office)
            return movie

    # def omdb_gat_by_year(self, year):
        
    
# film = Omdb()
# Film = film.omdb_get_by_id('tt7286456')
# print(Film.title, Film.release_date)




# class Get_movie:
#     def __init__(self, url, id):
#         self.url = url
#         # self.id = id
