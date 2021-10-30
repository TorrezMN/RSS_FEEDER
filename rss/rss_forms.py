#!/usr/bin/env python3
# encoding: utf-8
import curses
import npyscreen

from datetime import datetime
from faker import Faker as F

from db.db_toolkit import add_new_rss_feed
from db.db_toolkit import get_all_rss_feeds



class LIST_RSS( npyscreen.Form):

    OK_BUTTON_TEXT = 'DETAILS'

    def create(self):

        self.screen_size = self.curses_pad.getmaxyx() #(height,width)
        self.feeds = get_all_rss_feeds()
        self.selected_feed = None
        self.rss_list = self.add(
                npyscreen.MultiLine,
                name='RSS FEEDS AVIALABLE',
                values=[F().name() for i in range(0,100)],
                max_height= int(self.screen_size[0]*0.3),
                value = 0
                )
        #  self.rss_list.labelColor = 'GOOD'
        #  self.rss_list.when_cursor_moved = self.set_selected_feed
        self.rss_list.when_check_cursor_moved = curses.beep
        #  self.rss_list.when_value_edited = self.new_value_test


    def new_value_test(self):
        curses.beep
        npyscreen.notify_ok_cancel('CAMBIO EL VALOR{0}'.format(dir(self.rss_list)))



        
    def set_selected_feed(self):
        curses.beep
        #self.selected_feed = self.rss_list.value
        #self.selected_feed = self.rss_list.values[self.rss_list.value]
        #npyscreen.notify_ok_cancel('SELECCIONADO : {0}'.format(self.rss_list.__dict__))

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
