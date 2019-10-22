import argparse
import requests
from bs4 import BeautifulSoup

page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
soup = BeautifulSoup(page.content, 'html.parser')
# # print(soup.prettify())
# list(soup.children)
# html = list(soup.children)[2]
# body = list(html.children)[3]
# p = list(body.children)[1]
# print(p.get_text())
x = soup.find_all('p')[0].get_text
print(x)
