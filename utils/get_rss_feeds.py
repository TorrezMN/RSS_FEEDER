#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Torrez, MN
# Script that helps to fill db with data from https://blog.feedspot.com/software_development_rss_feeds/
# Dec. 2021

from datetime import datetime

import requests
from bs4 import BeautifulSoup as BS

BASE_URL = "https://blog.feedspot.com/technology_rss_feeds/"

if __name__ == '__main__':

    feeds = []
    req = requests.get(
        BASE_URL,
        headers={
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }).text
    soup = BS(req, 'lxml')

    mydiv = soup.find_all("div", {"class": "fsb"})

    #  new_rss = {
    #  'url': self.rss_url.value,
    #  'name': self.rss_name.value,
    #  'desc': self.rss_description.value,
    #  'created_date': datetime.today(),
    #  'status': True
    #  }

    rss_titles = mydiv[0].find_all('h3')

    rss_data = mydiv[0].find_all('p', {'class': 'trow-wrap'})

    print('wrap 1', rss_data[0])
