# Toutes les intéractions avec la base de données SQL
# Requêtes : INSERT, SELECT...

# -*- coding: utf-8 -*-

import mysql.connector
import socket
import time
import os
import json

from dotenv import load_dotenv
from pathlib import Path  # python3 only
load_dotenv()
env_path = Path('.') / 'auth.env'
load_dotenv(dotenv_path=env_path)

# MYSQL_CONNECTION = json.loads(environment)

class Db():

    def __init__(self):
        environment_string = os.getenv('MYSQL_CONNECTION')
        environment = json.loads(environment_string)
        self.user = environment['user']
        self.password = environment['password']
        self.host = environment['host']
        self.database = environment['database']

        self.is_ready = self.connectToDatabase(environment)

        self.cnx = mysql.connector.connect(
                        user=self.user,
                        password=self.password,
                        host=self.host,
                        database=self.database
                        )
        self.cursor = self.cnx.cursor(dictionary=True)


    """  Si on enlève la connexion dans l'initialisation  """
    # def _cnx(self):
    #     self.cnx = mysql.connector.connect(
    #                     user=self.user,
    #                     password=self.password,
    #                     host=self.host,
    #                     database=self.database
    #                     )
    #     self.cursor = self.cnx.cursor(dictionary=True)


    def isOpen(self,ip,port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, int(port)))
            s.shutdown(2)
            return True
        except:
            return False

    def connectToDatabase(self, environment):
        host = environment['host']
        while self.isOpen(host, 3306) == False:
            print("En attente de la BDD...")
            time.sleep(3)
        return host

    def get_cursor(self):
        return self.cursor
    
    def disconnect_database(self):
        self.cnx.close()

    def close_cursor(self):    
        self.cursor.close()
    
    def commit(self):
        self.cnx.commit()
