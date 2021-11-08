#!/usr/bin/env python3
# encoding: utf-8

import feedparser

from bs4 import BeautifulSoup
import requests
from collections import Counter
from operator import itemgetter



 

stop_words = [
    'i','me','my','myself','we','our','ours','ourselves','you','your','yours',
    'yourself','yourselves','he','him','his','himself','she','her','hers','herself',
    'it','its','itself','they','them','their','theirs','themselves','what','which',
    'who','whom','this','that','these','those','am','is','are',
    'was','were','be','been','being','have','has','had','having',
    'do','does','did','doing','a','an','the','and','but','if','or',
    'because','as','until','while','of','at','by','for','with','about',
    'against','between','into','through','during','before','after','above',
    'below','to','from','up','down','in','out','on','off','over','under',
    'again','further','then','once','here','there','when','where','why',
    'how','all','any','both','each','few',
    'more','most','other','some','such','no','nor',
    'not','only','own','same','so','than','too','very','s','t','can',
    'will','just','don','should','now']




URL = 'https://dev.to/jasonleowsg/secret-dev-tools-for-every-code-newbie-5a8a'

f = 'https://dev.to/feed/'



    
    



def get_news_stats(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')

    tl = soup.get_text().replace('\n','').replace('\n\n', '').replace('\n', '').replace('      ', '').replace('    ','').split(' ')


    curated = [i for i in tl if i.lower() not in stop_words]


    stats = Counter(curated)
    
    
    tags = []
    for k,v in enumerate(stats):
        if(k>100 and len(v)>6):
            tags.append([k,v])
    return({
        'url':url,
        'tags':sorted(tags, key=itemgetter(0), reverse=True),
        })

 


def get_news_from_rss(feed):
    
    f = feedparser.parse(feed[0].url)
    news = []
    
    for i in f['entries']:
        news.append(
            {
            'feed':feed[0].id,
            'author': i['author'],
            'date': i['published'],
            'title': i['title'],
            'url': i['link'],
            'tags': 'fasdfasdfa',
            }
        )
    return(news)


if __name__ == '__main__':
    print(get_news_stats(URL))
