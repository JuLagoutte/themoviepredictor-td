#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
TheMoviePredictor script
Author: Arnaud de Mouhy <arnaud@admds.net>
"""

import mysql.connector
import sys
import argparse
import csv

def connectToDatabase():
    return mysql.connector.connect(user='predictor', password='predictor',
                              host='127.0.0.1',
                              database='predictor')

def disconnectDatabase(cnx):
    cnx.close()

def createCursor(cnx):
    return cnx.cursor(dictionary=True)

def closeCursor(cursor):    
    cursor.close()

def findQuery(table, id):
    return ("SELECT * FROM {} WHERE id = {}".format(table, id))

def findAllQuery(table):
    return ("SELECT * FROM {}".format(table))

def find(table, id):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    query = findQuery(table, id)
    cursor.execute(query)
    results = cursor.fetchall()
    closeCursor(cursor)
    disconnectDatabase(cnx)
    return results

def findAll(table):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute(findAllQuery(table))
    results = cursor.fetchall()
    closeCursor(cursor)
    disconnectDatabase(cnx)
    return results

def insertPeopleQuery(table, firstname, lastname):
    return ("INSERT INTO {} (firstname, lastname) VALUES('{}', '{}')".format(table, firstname, lastname))

def insertPeople(table, firstname, lastname):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute(insertPeopleQuery(table, firstname, lastname))
    cnx.commit()
    closeCursor(cursor)
    disconnectDatabase(cnx)

def insertMovieQuery(table, title, original_title, synopsis, duration, rating, release_date):
    return ("INSERT INTO {} (title, original_title, synopsis, duration, rating, release_date) VALUES('{}', '{}', '{}', '{}', '{}','{}')".format(table, title, original_title, synopsis, duration, rating, release_date))

def insertMovie(table, title, original_title, synopsis, duration, rating, release_date):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute(insertMovieQuery(table, title, original_title, synopsis, duration, rating, release_date))
    cnx.commit()
    closeCursor(cursor)
    disconnectDatabase(cnx)

def printPerson(person):
    print("#{}: {} {}".format(person['id'], person['firstname'], person['lastname']))

def printMovie(movie):
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

args = parser.parse_args()

if args.context == "people":
    if args.action == "list":
        people = findAll("people")
        if args.export:
            with open(args.export, 'w', encoding='utf-8', newline='\n') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(people[0].keys())
                for person in people:
                    writer.writerow(person.values())
        else:
            for person in people:
                printPerson(person)
    if args.action == "find":
        peopleId = args.id
        people = find("people", peopleId)
        for person in people:
            printPerson(person)
    if args.action == "insert":
        if args.firstname and args.lastname:
            insertPeople("people", args.firstname, args.lastname)
            print('insert')

if args.context == "movies":
    if args.action == "list":  
        movies = findAll("movies")
        for movie in movies:
            printMovie(movie)
    if args.action == "find":  
        movieId = args.id
        movies = find("movies", movieId)
        for movie in movies:
            printMovie(movie)
    if args.action == "insert":
        if args.title:
            insertMovie("movies", args.title, args.original_title, args.synopsis, args.duration, args.rating, args.release_date)
            print('insert')