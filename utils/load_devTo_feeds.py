#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Torrez, MN
# Script that helps to fill db with data from https://blog.feedspot.com/software_development_rss_feeds/
# Dec. 2021

from datetime import datetime

import requests
from bs4 import BeautifulSoup as BS

BASE_URL = "https://dev.to/tags"


def add_dev_to_rss_feeds():
    feeds = []
    req = requests.get(
        BASE_URL,
        headers={
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }).text
    soup = BS(req, 'lxml')
    tags = soup.find_all("a", {"class": "crayons-tag"})

    for i in tags:
        f = {
            'url':
            "https://dev.to/feed/tag/{0}".format(i.text.replace('#', '')),
            'name': "DevTo RSS Feed for {0}".format(i.text),
            'desc': 'RSS Feed for articles with the {0} tag.'.format(i.text),
            'created_date': datetime.today(),
            'status': True
        }
        feeds.append(f)

    return (feeds)


if __name__ == '__main__':
    add_dev_to_rss_feeds()
