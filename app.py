#!/usr/bin/python 
# --> (c'est un shebang)
# -*- coding: utf-8 -*-

"""
TheMoviePredictor script
Author: Arnaud de Mouhy <arnaud@admds.net>
"""

import mysql.connector
import sys
import argparse
import csv
import requests
from bs4 import BeautifulSoup
from pprint import pprint 
from datetime import datetime
import locale
import os
import random

from movie import Movie
from person import Person
from omdb import Omdb
from tmdb import TheMoviedb
from all_api import All_api
from setparser import Parser
from db import Db

# if you work out the container
from dotenv import load_dotenv
from pathlib import Path  # python3 only
load_dotenv()
env_path = Path('.') / 'auth.env'
load_dotenv(dotenv_path=env_path)
#####################################

locale.setlocale(locale.LC_ALL, 'fr_FR')

api_key_tmdb = os.getenv('TMDB_API_KEY')
tmdb = TheMoviedb(api_key_tmdb)

api_key_omdb = os.getenv('OMDB_API_KEY')
omdb = Omdb(api_key_omdb)

all_api = All_api(api_key_tmdb, api_key_omdb)

db = Db()

def find_query(table, id):
    return (f"SELECT * FROM {table} WHERE id = {id} LIMIT 1")

def find_all_query(table):
    return (f"SELECT * FROM {table}")

def find(table, id):
    global db
    cursor = db.get_cursor()
    query = find_query(table, id)
    cursor.execute(query)
    results = cursor.fetchall()
    entity = None
    if (table == "movies"):
        if (cursor.rowcount == 1):
            row = results[0]
            entity = Movie(row['imdb_id'],
                        row['title'],
                        row['original_title'],
                        row['genre'],
                        row['synopsis'],
                        row['tagline'],
                        row['duration'],
                        row['production_budget'],
                        row['marketing_budget'],
                        row['release_date'],
                        row['rating'],
                        row['imdb_score'],
                        row['box_office'],
                        row['popularity'],
                        row['awards'],
                        row['is_3D']
            )
            entity.id = row['id']
    if (table == "people"):
        if (cursor.rowcount == 1):
            row = results[0]
            entity = Person(row['firstname'],
                            row['lastname'],
            )
            entity.id = row['id']
    return entity

def find_all(table):
    global db
    cursor = db.get_cursor()
    cursor.execute(find_all_query(table))
    results = cursor.fetchall() # liste de dictionnaires contenant des valeurs scalaires
    if (table == "movies"):
        movies = []
        for result in results: # dico avec Id, title...
            movie = Movie(
                imdb_id = result['imdb_id'], 
                title = result['title'], 
                original_title = result['original_title'],
                genre = result['genre'],
                synopsis = result['synopsis'],
                tagline = result['tagline'],
                duration = result['duration'],
                production_budget = result['production_budget'],
                marketing_budget = result['marketing_budget'],
                release_date = result['release_date'],
                rating = result['rating'],
                imdb_score = result['imdb_score'],
                box_office = result['box_office'],
                popularity = result['popularity'],
                awards = result['awards'],
                is_3D = result['is_3D']
            )
            movie.id = result['id']
            movies.append(movie)
        return movies
    if (table == "people"):
        people = []
        for result in results: # dico avec Id, firstname...
            person = Person(
                firstname = result['firstname'], 
                lastname = result['lastname'],
            )
            person.id = result['id']
            people.append(person)
        return people

def insert_people_query(person):
    add_person = ("INSERT INTO people "
                "(firstname, lastname) "
                "VALUES (%s, %s)")
    data_person = (person.firstname, person.lastname)
    return (add_person, data_person)

def insert_people(person):
    # pas besoin de signifier la table car c'est forcément la table People
    global db
    cursor = db.get_cursor()
    add_person, data_person = insert_people_query(person)
    cursor.execute(add_person, data_person)
    person.id = cursor.lastrowid
    db.commit()
    return cursor.lastrowid

def insert_movie_query(movie):
    add_movie = ("INSERT INTO movies "
                "(imdb_id, title, original_title, genre, synopsis, tagline, duration, production_budget, marketing_budget, release_date, rating, imdb_score, box_office, popularity, awards, is_3D) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    data_movie = (movie.imdb_id, movie.title, movie.original_title, movie.genre, movie.synopsis, movie.tagline, movie.duration, movie.production_budget, movie.marketing_budget, movie.release_date, movie.rating, movie.imdb_score, movie.box_office, movie.popularity, movie.awards, movie.is_3D)
    return (add_movie, data_movie)

def insert_movie(movie):
    global db
    cursor = db.get_cursor()
    add_movie, data_movie = insert_movie_query(movie)
    cursor.execute(add_movie, data_movie)
    movie.id = cursor.lastrowid
    db.commit()
    return cursor.lastrowid

def print_person(person):
    print(f"#{person.id}: {person.firstname} {person.lastname}")

def print_movie(movie):
    print(f"#{movie.id}: {movie.title} released on {movie.release_date}")  

parser = Parser()
args = parser.set_parser()

if args.context == "people":
    if args.action == "list":
        people = find_all("people")
        if args.export:
            with open(args.export, 'w', encoding='utf-8', newline='\n') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(people[0].__dict__.keys())
                for person in people:
                    writer.writerow(person.__dict__.values())
        else:
            for person in people:
                print_person(person)
    if args.action == "find":
        peopleId = args.id
        person = find("people", peopleId)
        if (person == None):
            print(f"Aucune personne avec l'id {peopleId} n'a été trouvé ! Try again !")
        else:
            print_person(person)
    if args.action == "insert":
        person = Person(args.firstname, 
                        args.lastname, 
        )
        person.id = insert_people(person)
        insert_people(person)
        print('insert')

if args.context == "movies":
    if args.action == "list":  
        movies = find_all("movies")
        for movie in movies:
            print_movie(movie)
    if args.action == "find":  
        movieId = args.id
        movie = find("movies", movieId)
        if (movie == None):
            print(f"Aucun film avec l'id {movieId} n'a été trouvé ! Try again !")
        else:
            print_movie(movie)
    if args.action == "insert":
        movie = Movie(args.title, 
                    args.original_title, 
                    args.genre,
                    args.synopsis,
                    args.tagline,
                    args.duration,
                    args.production_budget,
                    args.marketing_budget,
                    args.release_date, 
                    args.rating,
                    args.box_office,
                    args.popularity,
                    args.awards,
                    args.is_3D,
                    args.imdb_id, 
                    args.imdb_score
        )
        movie.id = insert_movie(movie)
        print('insert')

    # action "import", pour importer une base de données à partir d'un fichier csv ou à partir d'une API

    if args.action == "import":
        # if args.file:
        #     with open(args.file) as csvfile:
        #         csv_reader = csv.DictReader(csvfile, delimiter=',')
        #         for row in csv_reader:
        #             insert_movie(
        #                 row['title'],
        #                 row['original_title'],
        #                 row['genre'],
        #                 row['synopsis'],
        #                 row['tagline'],
        #                 row['duration'],
        #                 row['production_budget'],
        #                 row['marketing_budget'],
        #                 row['release_date'],
        #                 row['rating'],
        #                 row['imdb_score'],
        #                 row['box_office'],
        #                 row['popularity'],
        #                 row['awards'],
        #                 row['is_3D']
        #             )
        #             print(', '.join(row))
        if args.api == 'omdb':
            if args.imdb_id :
                movie = omdb.omdb_get_by_id(args.imdb_id)
                insert_movie(movie)
                print(f"insert {movie.id}")
        elif args.api == 'themoviedb':
            if args.imdb_id :
                movie = tmdb.tmdb_get_by_id(args.imdb_id)
                insert_movie(movie)
                print(f"insert {movie.id}")
        # elif args.api == 'all_api':
        #     if args.imdb_id:
        #         if args.imdb_id == 'random':
        #             a = random.randint(0, 9)
        #             b = random.randint(0, 9)
        #             c = random.randint(0, 9)
        #             d = random.randint(0, 9)
        #             e = random.randint(0, 9)
        #             f = random.randint(0, 9)
        #             g = random.randint(0, 9)
        #             searched_id = f"tt{a}{b}{c}{d}{e}{f}{g}"
        #             movie = all_api.get_by_id_imdb(searched_id)
        #             insert_movie(movie)
        #             print(f"insert {movie.id}")
        #         else:
        #             movie = all_api.get_by_id_imdb(args.imdb_id)
        #             insert_movie(movie)
        #             print(f"insert {movie.id}")
        
