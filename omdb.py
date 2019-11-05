import requests
import json
from pprint import pprint
from movie import Movie

with open('omdbapikey.txt', 'r') as file:
    apikey = file.read()

class Omdb:

    def omdb_get_by_id(self, id):
        r = requests.get(f'http://www.omdbapi.com/?i={id}&{apikey}')
        r = r.json()
        if r['Response'] == "False":
            movie = print(f"Aucun film avec l'id {id} n'existe dans OMDBapi")
            return movie
        else:
            title = r['Title']
            original_title = r['Title']
            release_date = r['Released']
            rating = "None"
            duration = r['Runtime']
            if r['Type']=="movie":
                box_office = r['BoxOffice']
            else:
                box_office = None
            omdb_id = r['imdbID']
            omdb_id = omdb_id.replace("tt", "")
            imdb_rating = r['imdbRating']

            movie = Movie(title, original_title, release_date, rating, duration, box_office, omdb_id, imdb_rating)
            return movie

    def omdb_gat_by_year(self, year):
        
    
# film = Omdb()
# print(film.omdb_get_by_id('tt8000000'))



# class Get_movie:
#     def __init__(self, url, id):
#         self.url = url
#         # self.id = id
