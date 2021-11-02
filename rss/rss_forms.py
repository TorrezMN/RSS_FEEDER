#!/usr/bin/env python3
# encoding: utf-8
import curses
import npyscreen
import random
from datetime import datetime
from faker import Faker as F

from db.db_toolkit import add_new_rss_feed
from db.db_toolkit import (get_all_rss_feeds,
                            filter_rss_title
                            )



class LIST_RSS(npyscreen.FormBaseNew):

    OK_BUTTON_TEXT = 'DETAILS'
    

    def create(self):
        self.keypress_timeout = 10
        self.screen_size = self.curses_pad.getmaxyx() #(height,width)
        self.feeds = get_all_rss_feeds()
        self.selected_feed = None
        self.rss_list = self.add(
                npyscreen.MultiLine,
                name='RSS FEEDS AVIALABLE',
                values = [i.name for i in self.feeds],
                max_height= int(self.screen_size[0]*0.3),
                value = 0
                )
        self.rss_list.when_check_cursor_moved = curses.beep
        

    def pre_edit_loop(self):
        curses.beep
        self.rss_list.values = [i.name for i in get_all_rss_feeds()]
        self.DISPLAY()

#  def while_waiting(self):
        #  npyscreen.notify_wait('AWAIT!')
        #  self.rss_list.values.append('test')
        #  self.DISPLAY()


    def afterEditing(self):
        npyscreen.notify_wait('VALOR: {0}'.format(self.selected_feed, title='RSS - DETAIL'))







class ADD_RSS(npyscreen.Popup, npyscreen.ActionForm):

    def create(self):
        self.name='NEW RSS FEED'
        self.rss_url = self.add(npyscreen.TitleText, name = "RSS URL:", value= "https://www.a_beautiful_rss.com" )
        self.rss_name = self.add(npyscreen.TitleText, name = "NAME:", value= "Name to identify the rss-feed." )
        self.rss_description = self.add(npyscreen.TitleText, name = "DESCRIPTION:", value= "Write a simple description about the origin of the RSS Feed." )
        self.rss_date_added = self.add(npyscreen.TitleDateCombo, name='DATE ADDED', value= datetime.today(),editable=False)

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
