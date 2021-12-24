#!/usr/bin/env python3
# encoding: utf-8
import curses
import npyscreen
import random
from datetime import datetime
from faker import Faker as F

from db.db_toolkit import add_new_rss_feed
from db.db_toolkit import (get_all_rss_feeds, filter_rss_title)


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
                                 max_height=int(self.screen_size[0] * 0.3),
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
        npyscreen.notify_wait('{0}'.format(add_new_rss_feed(f)))

    def on_cancel(self):
        npyscreen.notify_wait('CANSEL SAVE!', title='SAVING NEW RSS FEED')
        self.parentApp.switchForm('MAIN')
