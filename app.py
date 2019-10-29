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
from movie import Movie
from people import Person

locale.setlocale(locale.LC_ALL, 'fr_FR')


# # pour le scrapping

# r = requests.get("https://fr.wikipedia.org/wiki/Joker_(film,_2019)")
# soup = BeautifulSoup(r.content, 'html.parser')
# fiche_technique = soup.find(id="Fiche_technique")
# h2_tag = fiche_technique.parent
# ul_tag = h2_tag.find_next_sibling("ul")
# li_tags = ul_tag.find_all("li", recursive=False)

# for li_tag in li_tags:
#     splitted_li = li_tag.get_text().split(':')
#     data_type = splitted_li[0].strip()
#     data_value = splitted_li[1].strip()
    
#     if data_type == "Titre original":
#         title = data_value
#     if data_type == "Durée":
#         duration = data_value.replace("minutes", "").strip()
#     if data_type == "Dates de sortie":
#         release_dates_li_list = li_tag.find_all("li")
#         for release_date_li in release_dates_li_list:
#             release_date_splitted = release_date_li.get_text().split(':')
#             release_country = release_date_splitted[0].strip()
#             release_date_as_string = release_date_splitted[1].strip()  # 9 octobre 2019
#             if release_country == "France":
#                 release_date_object = datetime.strptime(release_date_as_string, '%d %B %Y')
#                 release_date_sql_string = release_date_object.strftime('%Y-%m-%d')
    
#     if data_type == "Classification":
#         ratings_li_list = li_tag.find_all("li")
#         for rating_li in ratings_li_list:
#             rating_splitted = rating_li.get_text().split(':')
#             rating_country = rating_splitted[0].strip()
#             rating_string = rating_splitted[1].strip()  # Interdit aux moins de 12 ans avec avertissement
#             if rating_country == "France":
#                 if rating_string.find('12') != -1:
#                     rating = '-12'

# print('Title = ', title)
# print('Duration = ', duration)
# print('Release_date = ', release_date_sql_string)
# print('rating = ', rating)


# exit()

##############

def connect_to_database():
    return mysql.connector.connect(user='predictor', password='predictor',
                              host='127.0.0.1',
                              database='predictor')

def disconnect_database(cnx):
    cnx.close()

def create_cursor(cnx):
    return cnx.cursor(dictionary=True)

def close_cursor(cursor):    
    cursor.close()

def find_query(table, id):
    return (f"SELECT * FROM {table} WHERE id = {id} LIMIT 1")

def find_all_query(table):
    return (f"SELECT * FROM {table}")

def find(table, id):
    cnx = connect_to_database()
    cursor = create_cursor(cnx)
    query = find_query(table, id)
    cursor.execute(query)
    results = cursor.fetchall()
    # entity = None
    movie = None
    person = None
    if (table == "movies"):
        if (cursor.rowcount == 1):
            row = results[0]
            movie = Movie(row['title'],
                          row['original_title'],
                          row['duration'],
                          row['release_date'],
                          row['rating']
            )
            movie.id = row['id']
        close_cursor(cursor)
        disconnect_database(cnx)
        return movie
    if (table == "people"):
        if (cursor.rowcount == 1):
            row = results[0]
            person = Person(row['firstname'],
                            row['lastname'],
            )
            person.id = row['id']
        close_cursor(cursor)
        disconnect_database(cnx)
        return person

def find_all(table):
    cnx = connect_to_database()
    cursor = create_cursor(cnx)
    cursor.execute(find_all_query(table))
    results = cursor.fetchall() # liste de dictionnaires contenant des valeurs scalaires
    close_cursor(cursor)
    disconnect_database(cnx)
    if (table == "movies"):
        movies = []
        for result in results: # dico avec Id, title...
            movie = Movie(
                title = result['title'], 
                original_title = result['original_title'],
                duration = result['duration'],
                release_date = result['release_date'],
                rating = result['rating']
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
    return (f"INSERT INTO people (firstname, lastname) VALUES('{person.firstname}', '{person.lastname}');")

def insert_people(person):
    # pas besoin de signifier la table car c'est forcément la table People
    cnx = connect_to_database()
    cursor = create_cursor(cnx)
    cursor.execute(insert_people_query(person))
    cnx.commit()
    close_cursor(cursor)
    disconnect_database(cnx)
    return cursor.lastrowid

def insert_movie_query(movie):
    return (f"INSERT INTO movies (title, original_title, duration, rating, release_date) VALUES('{movie.title}', '{movie.original_title}', '{movie.duration}', '{movie.rating}', '{movie.release_date}')")

def insert_movie(movie):
    cnx = connect_to_database()
    cursor = create_cursor(cnx)
    cursor.execute(insert_movie_query(movie))
    cnx.commit()
    close_cursor(cursor)
    disconnect_database(cnx)
    return cursor.lastrowid

def print_person(person):
    print(f"#{person.id}: {person.firstname} {person.lastname}")

def print_movie(movie):
    print(f"#{movie.id}: {movie.title} released on {movie.release_date}")

parser = argparse.ArgumentParser(description='Process MoviePredictor data')

parser.add_argument('context', choices=['people', 'movies'], help='Le contexte dans lequel nous allons travailler')

action_subparser = parser.add_subparsers(title='action', dest='action')

list_parser = action_subparser.add_parser('list', help='Liste les entitÃ©es du contexte')
list_parser.add_argument('--export' , help='Chemin du fichier exportÃ©')

find_parser = action_subparser.add_parser('find', help='Trouve une entitÃ© selon un paramÃ¨tre')
find_parser.add_argument('id' , help='Identifant Ã  rechercher')

insert_parser = action_subparser.add_parser('insert', help='insérer une donnée dans la database')
know_args = parser.parse_known_args()[0]

if know_args.context == "people":
    insert_parser.add_argument('--firstname', help='prenom', required=True)
    insert_parser.add_argument('--lastname', help='nom de famille', required=True)

if know_args.context == "movies":
    insert_parser.add_argument('--title', help='le titre en france', required=True)
    insert_parser.add_argument('--original_title', help='titre original', required=True)
    insert_parser.add_argument('--synopsis', help='le synopsis du film')
    insert_parser.add_argument('--duration', help='la durée en minute du film', required=True)
    insert_parser.add_argument('--rating', help='la classification pour visionnage du public', choices=('TP', '-12', '-16', '-18'), required=True)
    insert_parser.add_argument('--production_budget', help='le budget du film')
    insert_parser.add_argument('--marketing_budget', help='le budget pour la promo du film')
    insert_parser.add_argument('--release_date', help='la date de sortie', required=True)

import_parser = action_subparser.add_parser('import', help='Importer de nouvelles données')
import_parser.add_argument('--file', help='nom du fichier à recuperer')

args = parser.parse_args()

if args.context == "people":
    if args.action == "list":
        people = find_all("people")
        if args.export:
            with open(args.export, 'w', encoding='utf-8', newline='\n') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(people[0].keys())
                for person in people:
                    writer.writerow(person.values())
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
                       args.duration, 
                       args.release_date, 
                       args.rating
                )
        movie.id = insert_movie(movie)
        print('insert')

    # action "import", pour importer une base de données à partir d'un fichier csv
    # if args.action == "import":
    #     if args.file:
    #         with open(args.file) as csvfile:
    #             csv_reader = csv.DictReader(csvfile, delimiter=',')
    #             for row in csv_reader:
    #                 insert_movie(
    #                     row['title'], 
    #                     row['original_title'], 
    #                     row['duration'], 
    #                     row['rating'], 
    #                     row['release_date']
    #                 )
    #                 print(', '.join(row))