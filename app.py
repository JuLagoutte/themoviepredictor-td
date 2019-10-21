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
    return (f"SELECT * FROM '{table}' WHERE id = {id}")

def find_all_query(table):
    return (f"SELECT * FROM '{table}'")

def find(table, id):
    cnx = connect_to_database()
    cursor = create_cursor(cnx)
    query = find_query(table, id)
    cursor.executemany(query)
    results = cursor.fetchall()
    close_cursor(cursor)
    disconnect_database(cnx)
    return results

def find_all(table):
    cnx = connect_to_database()
    cursor = create_cursor(cnx)
    cursor.execute(find_all_query(table))
    results = cursor.fetchall()
    close_cursor(cursor)
    disconnect_database(cnx)
    return results

def insert_people_query(firstname, lastname):
    return (f"INSERT INTO 'people' (firstname, lastname) VALUES('{firstname}', '{lastname}');")

def insert_people(firstname, lastname):
    # pas besoin de signifier la table car c'est forcément la table People
    cnx = connect_to_database()
    cursor = create_cursor(cnx)
    cursor.execute(insert_people_query(firstname, lastname))
    cnx.commit()
    close_cursor(cursor)
    disconnect_database(cnx)

def insert_movie_query(title, original_title, duration, rating, release_date):
    return (f"INSERT INTO 'movies' (title, original_title, duration, rating, release_date) VALUES('{title}', '{original_title}', '{duration}', '{rating}', '{release_date}')")

def insert_movie(title, original_title, duration, rating, release_date):
    cnx = connect_to_database()
    cursor = create_cursor(cnx)
    cursor.execute(insert_movie_query(title, original_title, duration, rating, release_date))
    cnx.commit()
    close_cursor(cursor)
    disconnect_database(cnx)

def print_person(person):
    print("#{}: {} {}".format(person['id'], person['firstname'], person['lastname']))

def print_movie(movie):
    print("#{}: {} released on {}".format(movie['id'], movie['title'], movie['release_date']))

parser = argparse.ArgumentParser(description='Process MoviePredictor data')

parser.add_argument('context', choices=['people', 'movies'], help='Le contexte dans lequel nous allons travailler')

action_subparser = parser.add_subparsers(title='action', dest='action')

list_parser = action_subparser.add_parser('list', help='Liste les entitÃ©es du contexte')
list_parser.add_argument('--export' , help='Chemin du fichier exportÃ©')

find_parser = action_subparser.add_parser('find', help='Trouve une entitÃ© selon un paramÃ¨tre')
find_parser.add_argument('id' , help='Identifant Ã  rechercher')

insert_parser = action_subparser.add_parser('insert', help='insérer une donnée dans la database')
insert_parser.add_argument('--firstname', help='prenom')
insert_parser.add_argument('--lastname', help='nom de famille')
# insert_parser.parse_known_args()

insert_parser.add_argument('--title', help='le titre en france')
insert_parser.add_argument('--original_title', help='titre original')
insert_parser.add_argument('--synopsis', help='le synopsis du film')
insert_parser.add_argument('--duration', help='la durée en minute du film')
insert_parser.add_argument('--rating', help='la classification pour visionnage du public')
insert_parser.add_argument('--production_budget', help='le budget du film')
insert_parser.add_argument('--marketing_budget', help='le budget pour la promo du film')
insert_parser.add_argument('--release_date', help='la date de sortie')

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
        people = find("people", peopleId)
        for person in people:
            print_person(person)
    if args.action == "insert":
        if args.firstname and args.lastname:
            insert_people(args.firstname, args.lastname)
            print('insert')

if args.context == "movies":
    if args.action == "list":  
        movies = find_all("movies")
        for movie in movies:
            print_movie(movie)
    if args.action == "find":  
        movieId = args.id
        movies = find("movies", movieId)
        for movie in movies:
            print_movie(movie)
    if args.action == "insert":
        if args.title:
            insert_movie(args.title, args.original_title, args.duration, args.rating, args.release_date)
            print('insert')
    if args.action == "import":
        if args.file:
            with open(args.file) as csvfile:
                csv_reader = csv.DictReader(csvfile, delimiter=',')
                for row in csv_reader:
                    insert_movie(row['title'], row['original_title'], row['duration'], row['rating'], row['release_date'])
                    print(', '.join(row))
