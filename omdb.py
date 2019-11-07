import requests
import json
from pprint import pprint
from movie import Movie
from datetime import datetime
import locale
import isodate

locale.setlocale(locale.LC_ALL, 'en_US')


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
            # release_date_class = r['Released']
            # # release_date_splitted = release_date_class.split(' ')
            # release_date_object = datetime.strptime(release_date_class, '%d %B %Y')
            # # release_date = release_date_object.strftime('%Y-%m-%d')
            rating = "None"
            duration = r['Runtime']
            duration = duration.split()
            duration = duration[0]
            if r['Type']=="movie":
                box_office = r['BoxOffice']
            else:
                box_office = None
            omdb_id = r['imdbID']
            omdb_id = omdb_id.replace("tt", "")
            imdb_score = r['imdbRating']

            movie = Movie(omdb_id, title, original_title, duration, release_date_object, rating, imdb_score, box_office)
            print(release_date_object)
            return movie

    # def omdb_gat_by_year(self, year):
        
    
film = Omdb()
print(film.omdb_get_by_id('tt7286456'))



# class Get_movie:
#     def __init__(self, url, id):
#         self.url = url
#         # self.id = id
