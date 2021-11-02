#!/usr/bin/env python3
# encoding: utf-8

import npyscreen
import urwid



# Importing forms.
from rss.rss_forms import ADD_RSS
from rss.rss_forms import LIST_RSS


# DB
from db.db_engine import db
from db.db_engine import initialize_db



def cls():
    npyscreen.blank_terminal()




class MainForm(npyscreen.FormBaseNewWithMenus, npyscreen.SplitForm):
    def create(self):
        self.screen_size = self.curses_pad.getmaxyx() #(height,width)
        self.half_way = self.get_half_way()



        self.add(
            npyscreen.FixedText,
            value='Simulate social network activity with RSS FEEDER.',
            relx= int(self.screen_size[1]*0.5)-25, 
            rely= int(self.screen_size[0]*0.5),
            width=50, 
            height=15,
            color='GOOD'
        )
        self.add(
            npyscreen.FixedText,
            value='Linkedin - Twitter',
            relx= int(self.screen_size[1]*0.5)-int(len('Linkedin - Twitter')*0.5), 
            rely= int(self.screen_size[0]*0.5)+1,
            width=50, 
            height=15,
            color='GOOD'
        )   
        
        # MAIN MENU
        self.menu = self.add_menu(name="Main Menu", shortcut="^M")
        # RSS FEEDS
        self.rss_submenu = self.menu.addNewSubmenu('RSS', shortcut='r')
        self.rss_submenu.addItem('ADD RSS FEED', self.add_rss, shortcut='a')
        self.rss_submenu.addItem('LIST RSS FEED', self.list_rss, shortcut='s')
        self.rss_submenu.addItem('SEARCH RSS FEED', self.search_rss, shortcut='f')
        # ARTICLES
        self.articles_submenu = self.menu.addNewSubmenu('ARTICLES', shortcut='a')
        # TWITTER
        self.twitter_submenu = self.menu.addNewSubmenu('TWITTER', shortcut='t')
        # CONFIG
        self.config_submenu = self.menu.addNewSubmenu('CONFIG', shortcut='c')
        
        # MAIN MENU ITEMS
        self.menu.addItem('EXIT APP', self.exitAplication, shortcut='s')

    def exitAplication(self):
        self.parentApp.switchForm(None)
        cls()

    def add_rss(self):
        self.parentApp.switchForm('ADD_RSS_FEED')
        cls()


    def search_rss(self):
        pass

    def list_rss(self):
        self.parentApp.switchForm('LIST_RSS_FEED')
        cls()



class RSS_FEEDER(npyscreen.NPSAppManaged):

        
    keypress_timeout_default = 50

    def onStart(self):
        initialize_db()
               

        self.registerForm('MAIN', MainForm(name='RSS FEEDER'))
        # RSS FEED
        self.registerForm('ADD_RSS_FEED', ADD_RSS(name='ADD RSS FEED'))
        self.registerForm('LIST_RSS_FEED', LIST_RSS(name='LIST RSS FEED'))


if __name__ == "__main__":
    RSF = RSS_FEEDER()
    RSF.run()
    
