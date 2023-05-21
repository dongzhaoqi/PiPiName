# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 12:03:06 2020

@author: kun
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent

ua = UserAgent()

headers = {
    'user-agent': ua.random,
    'Host': 'movie.douban.com'
}


def get_movies():
    movie_list = []
    for i in range(0, 10):
        link = 'https://movie.douban.com/top250?start=' + str(i * 25)
        r = requests.get(link, headers=headers, timeout=10)

        soup = BeautifulSoup(r.content)
        div_list = soup.find_all('div', class_='info')
        for movie in div_list:
            title = movie.find('div', class_='hd').a.span.text.strip()
            info = movie.find('div', class_='bd').p.text.strip()
            info = info.replace("\n", " ").replace("\xa0", " ")
            info = ' '.join(info.split())
            rating = movie.find('span', class_='rating_num').text.strip()
            num_rating = movie.find('div', class_='star').contents[7].text.strip()
            try:
                quote = movie.find('span', class_='inq').text.strip()
            except:
                quote = ""

            movie_list.append([title, info, rating, num_rating, quote])
        df = pd.DataFrame(movie_list, columns=['电影名称', '信息', '评分', '评价人数', '短评'], index=None)

        df.to_csv("douban.csv")
    return movie_list


movies = get_movies()
print(movies)
