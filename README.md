# the-movie-predictor-JuLagoutte
the-movie-predictor-JuLagoutte created by GitHub Classroom

## Objectifs du README : 

* Connaître les objectifs du projet the moviepredictor-td
* Savoir comment démarrer le projet
* Savoir comment travailler avec les fichiers du projet

## Objectifs du projet themoviepredictor-td :

* Créer une base de données de films complètes
* Remplir la base de données à partir de scrapping, de l'utilisation d'API ou à partir du traitement d'un fichier brut du site IMDB
* __objectif final__ : en utilisant le processus de machine learning, prédire une note spectateur du film 2 semaines après sa sortie en salle

## Etapes pour démarrer le projet themoviepredictor :

1. git clone ou fork
2. création d'un fichier auth.env pour stocker les variables d'environnement:
* contenu du fichier auth.env
3. pour obtenir les variables d'environnement (clés d'API) :
4. pour lancer le projet une fois tout installé : (commande docker-compose...)

## Table des matières (contenu du repository) :

* [app.py](https://github.com/JuLagoutte/themoviepredictor-td/blob/master/app.py) :
  _script général du projet_ (mettre exemples de commandes)
* [scrap.py](https://github.com/JuLagoutte/themoviepredictor-td/blob/master/scrap.py) :
  _script pour scrapper sur wikipédia_
* [omdb.py](https://github.com/JuLagoutte/themoviepredictor-td/blob/master/omdb.py) :
  _class Omdb pour utiliser l'API OMDB pour ajouter des films dans la base avec une commande du script app.py_
* [tmdb.py](https://github.com/JuLagoutte/themoviepredictor-td/blob/master/tmdb.py) :
  _class TheMoviedb pour utiliser l'API TMDB pour ajouter des films dans la base avec une commande du script app.py_
* [movie.py](https://github.com/JuLagoutte/themoviepredictor-td/blob/master/movie.py)
  _class Movie utilisée dans le script app.py_
* [person.py](https://github.com/JuLagoutte/themoviepredictor-td/blob/master/person.py)
  _class Person utilisée dans le script app.py_
* [db.py](https://github.com/JuLagoutte/themoviepredictor-td/blob/master/db.py) : 
  _class DB utilisée pour toutes les intéractions avec la base de données MySQL_
* [docker-compose.yml](https://github.com/JuLagoutte/themoviepredictor-td/blob/master/docker-compose.yml) :
  _sert pour la mise en route des containers nécessaires au projet_
* [Dockerfile](https://github.com/JuLagoutte/themoviepredictor-td/blob/master/Dockerfile) : 
  _dossier pour la création de l'image docker_
* [.dockerignore](https://github.com/JuLagoutte/themoviepredictor-td/blob/master/.dockerignore)
  _équivalent de gitignore pour docker, tous les fichiers à ne pas partager lors de la publication de l'image_
* [.gitignore](https://github.com/JuLagoutte/themoviepredictor-td/blob/master/.gitignore)
  _tous les fichiers à ne pas committer dans git_
* [TheMoviePredictor_create.sql](https://github.com/JuLagoutte/themoviepredictor-td/blob/master/TheMoviePredictor_create.sql)
  _Base de données MySQL_

