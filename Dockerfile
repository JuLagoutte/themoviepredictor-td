FROM python:3.7-alpine

RUN pip install argparse requests mysql-connector-python beautifulsoup4 isodate

COPY . /usr/src/themoviepredictor

WORKDIR /usr/src/themoviepredictor

# CMD python /usr/src/themoviepredictor/app.py movies import--api all --for 7
# utilisation de CMD quand on voudra automatiser une mise à jour de la base de données SQL 
# (ex : requête une fois par semaine pour avori tous les nouveaux films)