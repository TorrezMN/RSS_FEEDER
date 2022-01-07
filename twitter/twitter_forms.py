#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Torrez, MN

import curses
import itertools
import time

import npyscreen

from db.db_engine import News, RSS_Feed
from db.db_toolkit import (add_news, delete_news, filter_news_title,
                           get_all_rss_feeds, get_list_articles)
from twitter.twitter_engine import TwitterEngine
from utils.utilities import get_news_from_rss, get_news_stats


def cls():
    npyscreen.blank_terminal()


class MY_TWITTER_FEED(npyscreen.FormBaseNew):
    def create(self):
        self.screen_size = self.curses_pad.getmaxyx()  #(height,width)
        self.te = TwitterEngine()

        self.add(npyscreen.FixedText,
                 value='MY TWITTER FEED',
                 relx=int(self.screen_size[1] * 0.5 - 6),
                 rely=int(self.screen_size[0] * 0.05),
                 width=50,
                 height=15,
                 color='GOOD')

        self.tweets_list = [i['text'] for i in self.te.get_twitter_time_line()]

        self.feed = self.add(npyscreen.MultiLine,
                             name='FEED',
                             values=self.tweets_list,
                             max_height=int(self.screen_size[0] * 0.6),
                             value=0,
                             color='GOOD')
        self.rss_go_back_btn = self.add(
            npyscreen.ButtonPress,
            when_pressed_function=self.go_back_pressed,
            name='GO BACK',
            relx=int(self.screen_size[1] * 0.8),
            rely=int(self.screen_size[0] * 0.9),
        )

    def go_back_pressed(self):
        self.parentApp.switchForm('MAIN')
