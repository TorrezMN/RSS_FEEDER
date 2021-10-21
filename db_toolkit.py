from peewee import *


import html2text

from datetime import datetime
import feedparser
import requests
from random import choice
import time
from faker import Faker as F

#  Importing models.
from db_engine import (RSS_Feed, News)
from db_engine import db 
from db_engine import initialize_db



def add_new_rss_feed(feed):
    if(check_rss_active_status(feed['url'])):
            #  db.connect()
            try:
                RSS_Feed.create(
			url = feed['url'],
                        name= feed['name'],
                        description = feed['desc'],
			created_date = feed['created_date'],
			feed_status = feed['status'],
			).save()
            except IntegrityError:
                print('RSS URL Already saved.')
            db.close()
    else:
        return('URL IS OUT OF LINE')

def get_all_rss_feeds():
    return(RSS_Feed.select())

def check_rss_active_status(url):
    try:
        req = requests.get(url)
        if(req.status_code==200):
            return (True)
    except requests.exceptions.ConnectionError:
        return(False)


def get_list_articles():
    return(News.select())


def get_news_feeds(url, feed_origin):
    feed = feedparser.parse(url)
    for i in feed.entries:
        try:
            News.create(
                feed  =  feed_origin,
                author  =  i.author,
                published_date  =  i.published,
                title  =  i.title_detail.value,
                link_url  =  i.link,
                article_tags  =  ''.join([i.term+', ' for i in i.tags]),
            ).save()
            
        except IntegrityError:
            pass
            
                

