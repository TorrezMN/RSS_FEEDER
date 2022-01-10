from peewee import *

import time
import requests
import npyscreen
import feedparser
from random import choice
from faker import Faker as F
from datetime import datetime

#  Importing models.
from db.db_engine import db
from db.db_engine import initialize_db
from db.db_engine import (RSS_Feed, News)


def check_rss_active_status(url):
    if (len(url) > 0):
        try:
            req = requests.get(url)
            if (req.status_code == 200):
                return (True)
        except requests.exceptions.ConnectionError:
            return (False)


def get_all_rss_feeds():
    return (RSS_Feed.select())


def get_list_articles():
    return (News.select())


def add_new_rss_feed(feed):
    if (check_rss_active_status(feed['url'])):
        #  db.connect()
        try:
            RSS_Feed.create(
                url=feed['url'],
                name=feed['name'],
                description=feed['desc'],
                created_date=feed['created_date'],
                feed_status=feed['status'],
            ).save()
        except IntegrityError:
            print('RSS URL Already saved.')
            #  db.close()
    else:
        return ('URL IS OUT OF LINE')


def add_news(news):
    try:
        News.create(feed=news['feed'],
                    author=news['author'],
                    published_date=news['date'],
                    title=news['title'],
                    link_url=news['url'],
                    article_tags=news['tags']).save()
    except IntegrityError:
        print('NEWS WAS ALREADY SAVED')


def filter_rss_title(title):
    rss = RSS_Feed.select().where(RSS_Feed.name.contains(str(title)))
    return (rss)


def filter_news_title(title):
    news = News.select().where(News.title.contains(str(title)))
    return (news)


def delete_news(news_title):
    news = News.get(News.title == news_title)
    news.delete_instance()
