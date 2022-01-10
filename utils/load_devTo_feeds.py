#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Torrez, MN
# Script that helps to fill db with data from https://blog.feedspot.com/software_development_rss_feeds/
# Dec. 2021

from datetime import datetime

import requests
from bs4 import BeautifulSoup as BS

BASE_URL = "https://dev.to/tags"


def add_rss_feeds():
    feeds = []
    req = requests.get(
        BASE_URL,
        headers={
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }).text
    soup = BS(req, 'lxml')
    mydivs = soup.find_all("div", {"class": "tag-card"})

    print('TAGS SIZE: ', len(mydivs))


if __name__ == '__main__':
    add_rss_feeds()
