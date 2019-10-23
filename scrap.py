import mysql.connector
import sys
import argparse
import csv
import requests
from bs4 import BeautifulSoup
from pprint import pprint 
from datetime import datetime
import locale


# https://www.imdb.com/title/tt0456123/  Dikkenek
# https://www.imdb.com/title/tt2527338/  Star Wars
# https://www.imdb.com/title/tt7286456/  Joker

locale.setlocale(locale.LC_ALL, 'en_US')


r = requests.get("https://www.imdb.com/title/tt0456124/", headers={'Accept-Language' : "fr-FR"})
soup = BeautifulSoup(r.content, 'html.parser')

title_wrapper = soup.find(class_="title_wrapper")
title_class = title_wrapper.find_next("h1")
splitted_title = title_class.get_text().split('(')
title = splitted_title[0].strip()


original_title_class = soup.find(class_="originalTitle")
if original_title_class:
    splitted_original_title = original_title_class.get_text().split('(')
    original_title = splitted_original_title[0].strip()
else:
    original_title = title

rating_class = title_wrapper.find_next(class_="subtext")
splitted_rating = rating_class.get_text().split('|')
rating_string = splitted_rating[0].strip()
if rating_string.find('Tous') != -1:
    rating = 'TP'
elif rating_string.find('12') != -1:
    rating = '-12'
elif rating_string.find('16') != -1:
    rating = '-16'
elif rating_string.find('18') != -1:
    rating = '-18'
else:
    rating = 'TP'

duration_class = rating_class.find_next("time")
# duration_s = isodate.parse_duration("PT84M")
# duration = int(duration_s.total_seconds()/60)
splitted_duration = duration_class.get_text().split('h')
h_splitted_duration = int(splitted_duration[0])*60
m_splitted_duration = int(splitted_duration[1].replace('min', ''))
duration = h_splitted_duration + m_splitted_duration
# ne fonctionne pas si le film dure moins de 1h

release_date_class = soup.find(title="See more release dates")
splitted_release_date = release_date_class.get_text().split('(')
release_date = splitted_release_date[0].strip()
release_date_object = datetime.strptime(release_date, '%d %B %Y')
release_date_sql_string = release_date_object.strftime('%Y-%m-%d')

print('Title = ', title)
print('Original_title =', original_title)
print('Duration = ', duration)
print('Release_date = ', release_date_sql_string)
print('rating = ', rating)