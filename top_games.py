'''Look through the top games of boardgamegeek,
and list the top 5000 games'''

import requests
from bs4 import BeautifulSoup

def top_games():

    top_games = []

    for page in range(1,51):
        url = f'https://boardgamegeek.com/search/boardgame/page/{page}?advsearch=1&q=&include%5Bdesignerid%5D=&include%5Bpublisherid%5D=&geekitemname=&range%5Byearpublished%5D%5Bmin%5D=&range%5Byearpublished%5D%5Bmax%5D=&range%5Bminage%5D%5Bmax%5D=&range%5Bnumvoters%5D%5Bmin%5D=500&range%5Bnumweights%5D%5Bmin%5D=&range%5Bminplayers%5D%5Bmax%5D=&range%5Bmaxplayers%5D%5Bmin%5D=&range%5Bleastplaytime%5D%5Bmin%5D=&range%5Bplaytime%5D%5Bmax%5D=&floatrange%5Bavgrating%5D%5Bmin%5D=&floatrange%5Bavgrating%5D%5Bmax%5D=&floatrange%5Bavgweight%5D%5Bmin%5D=&floatrange%5Bavgweight%5D%5Bmax%5D=&colfiltertype=&searchuser=Hrein&playerrangetype=normal&B1=Submit'
        response = requests.get(url)
        soup =  BeautifulSoup(response.content, "html.parser")
        game_names = [entry.text for entry in soup.find_all('a', class_='primary')]
        top_games += game_names

    return top_games