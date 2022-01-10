#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Torrez, MN
# Script that helps to fill db with data from https://blog.feedspot.com/software_development_rss_feeds/
# Dec. 2021

from datetime import datetime

import requests
from bs4 import BeautifulSoup as BS

BASE_URL = "https://blog.feedspot.com/technology_rss_feeds/"


def add_rss_feeds():

    feeds = []
    req = requests.get(
        BASE_URL,
        headers={
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }).text
    soup = BS(req, 'lxml')

    mydiv = soup.find_all("div", {"class": "fsb"})
    rss_titles = mydiv[0].find_all('h3')
    rss_data = mydiv[0].find_all('p', {'class': 'trow-wrap'})

    #  FIND TITLES
    for i in rss_titles:
        for j in i.find_all('a'):
            feeds.append({'name': j.text})

    #  PRINT HIPPERLINK
    for j, k in enumerate(rss_data):
        hrefs = k.find_all('a')
        feeds[j]['url'] = hrefs[0]['href']

    #  GETTING THE DESCRIPTION TEXT
    for j, k in enumerate(rss_data):
        feeds[j]['desc'] = k.text

    #  ADDING DATE AND STATUS

    for i in feeds:
        i['created_date'] = datetime.today()
        i['status'] = True

    return (feeds)


if __name__ == '__main__':
    for i in add_rss_feeds():
        print('---->', i['url'])
