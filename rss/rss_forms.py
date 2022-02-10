#!/usr/bin/env python3
# encoding: utf-8
import curses
import random
from datetime import datetime

import npyscreen
from faker import Faker as F

from db.db_toolkit import (add_new_rss_feed, filter_news_by_rss_feed,
                           filter_rss_title, get_all_rss_feeds)


class LIST_RSS(npyscreen.FormBaseNew):

    OK_BUTTON_TEXT = 'DETAILS'

    def create(self):
        self.keypress_timeout = 10
        self.screen_size = self.curses_pad.getmaxyx()  #(height,width)
        self.feeds = get_all_rss_feeds()
        self.selected_feed = None
        self.rss_list = self.add(npyscreen.MultiLine,
                                 name='RSS FEEDS AVIALABLE',
                                 values=[i.name for i in self.feeds],
                                 max_height=int(self.screen_size[0] * 0.7),
                                 value=0)
        self.rss_list.when_check_cursor_moved = curses.beep
        self.rss_detail_btn = self.add(
            npyscreen.ButtonPress,
            when_pressed_function=self.detail_pressed,
            name='RSS DETAIL',
            relx=int(self.screen_size[1] * 0.6),
            rely=int(self.screen_size[0] * 0.9))
        self.rss_go_back_btn = self.add(
            npyscreen.ButtonPress,
            when_pressed_function=self.go_back_pressed,
            name='GO BACK',
            relx=int(self.screen_size[1] * 0.8),
            rely=int(self.screen_size[0] * 0.9),
        )

    def go_back_pressed(self):
        self.parentApp.switchForm('MAIN')

    def detail_pressed(self):
        selected_index = self.rss_list.value
        npyscreen.notify_ok_cancel('SELECCIONADO : {0}'.format(
            self.rss_list.values[selected_index]))

    def pre_edit_loop(self):
        curses.beep
        self.rss_list.values = [i.name for i in get_all_rss_feeds()]
        self.DISPLAY()


class ADD_RSS(npyscreen.Popup, npyscreen.ActionForm):

    def create(self):
        self.name = 'NEW RSS FEED'
        self.rss_url = self.add(npyscreen.TitleText,
                                name="RSS URL:",
                                value="https://www.a_beautiful_rss.com")
        self.rss_name = self.add(npyscreen.TitleText,
                                 name="NAME:",
                                 value="Name to identify the rss-feed.")
        self.rss_description = self.add(
            npyscreen.TitleText,
            name="DESCRIPTION:",
            value="Write a simple description about the origin of the RSS Feed."
        )
        self.rss_date_added = self.add(npyscreen.TitleDateCombo,
                                       name='DATE ADDED',
                                       value=datetime.today(),
                                       editable=False)

    def on_ok(self):
        npyscreen.notify_wait('OK SAVE!', title='SAVING NEW RSS FEED')
        f = {
            'url': self.rss_url.value,
            'name': self.rss_name.value,
            'desc': self.rss_description.value,
            'created_date': self.rss_date_added.value,
            'status': True
        }

    def on_cancel(self):
        npyscreen.notify_wait('CANSEL SAVE!', title='SAVING NEW RSS FEED')
        self.parentApp.switchForm('MAIN')


class InputBox(npyscreen.BoxTitle):
    # MultiLineEdit now will be surrounded by boxing
    _contained_widget = npyscreen.MultiLine


class LIST_RSS_BY_TOPIC(npyscreen.ActionForm):

    def create(self):
        self.name = 'LIST RSS FEED by TOPIC'
        y, x = self.useable_space()
        self.rss_topics = self.add(
            npyscreen.BoxTitle,
            name="RSS Topics",
            custom_highlighting=True,
            value=0,
            values=[
                i.name if x > 80 else i.name.replace(' RSS Feed for ', '->')
                for i in get_all_rss_feeds()
            ],
            max_width=int(x * 0.3),
            max_height=int(y * 0.8))

        self.rss_topics.when_value_edited = self.topic_changed
        self.news_by_feed = self.add(InputBox,
                                     name="RELATED ARTICLES",
                                     footer="footer",
                                     max_width=int(x * 0.6),
                                     max_height=int(y * 0.8),
                                     relx=int(x * 0.33),
                                     rely=2)

        #  npyscreen.notify_ok_cancel('rss_topics {0}'.format(
        #  dir(self.news_by_feed)))

    def topic_changed(self):
        rss = self.rss_topics.values[self.rss_topics.value].split('#')[1]
        self.news_by_feed.entry_widget.values = [
            '> ' + i.title for i in filter_news_by_rss_feed(rss)
        ]
        self.news_by_feed.footer = 'Showing all news related to [{0}] feed.'.format(
            rss.upper())
        self.DISPLAY()
