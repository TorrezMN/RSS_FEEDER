#!/usr/bin/env python3
# encoding: utf-8

import npyscreen
import urwid


# Importing forms.
from rss.rss_forms import ADD_RSS


def cls():
    npyscreen.blank_terminal()




class RSS_FEEDER(npyscreen.NPSAppManaged):

    def onStart(self):
        self.registerForm('MAIN', MainForm(name='RSS FEEDER'))
        # RSS FEED
        self.registerForm('ADD_RSS_FEED', ADD_RSS(name='ADD RSS FEED'))




class MainForm(npyscreen.FormBaseNewWithMenus, npyscreen.SplitForm):
    def create(self):
        
        self.half_way = self.get_half_way()
        self.add(npyscreen.TitleMultiLine, value= "A simple application to simulate social network activity.", relx= 20, rely= self.half_way,width=40, height=10,color='GOOD')
        
        

        # MAIN MENU
        self.menu = self.add_menu(name="Main Menu", shortcut="^M")
        # RSS FEEDS
        self.rss_submenu = self.menu.addNewSubmenu('RSS', shortcut='r')
        self.rss_submenu.addItem('ADD RSS FEED', self.add_rss, shortcut='a')
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




if __name__ == "__main__":
    RSF = RSS_FEEDER()
    RSF.run()