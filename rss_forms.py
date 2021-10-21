import npyscreen
import pyttsx3
import curses
from datetime import datetime
import time
from db_toolkit import (get_list_articles,
                        get_all_rss_feeds,
                        add_new_rss_feed,
                        get_news_feeds)

 
def cls():
    npyscreen.blank_terminal()



class ListRssFeed(npyscreen.FormBaseNew):
    def create(self):
        self.name='LIST OF RSS FEEDS]'
        self.rss_list = [i.name for i in get_all_rss_feeds()]
        self.title = self.add(npyscreen.TitleText, name = "TOTAL:", value= "{0}".format(len(get_all_rss_feeds())) , editable = False)
        self.option_selected = self.add(npyscreen.TitleSelectOne, name='RSS FEEDS LIST', values = self.rss_list)
        

        
        self.option_selected.when_cursor_moved = curses.beep
        

    def shit_moved(self):
        npyscreen.notify_ok_cancel('SHIT MOVED RIGHT THERE!')


    def pre_edit_loop(self):
        cls()
        self.rss_list = [i.name for i in get_all_rss_feeds()]

    def afterEditing(self):
        detail_notify = npyscreen.notify_ok_cancel('RESULTADO {0}'.format(self.option_selected.value), title='RSS DETAILS')
        if(detail_notify==True):
            self.parentApp.switchForm('MAIN')
        else:
            self.parentApp.switchForm('LISTFEED')
    
class AddRssFeed(npyscreen.Popup, npyscreen.ActionForm):

    def create(self):
        self.name='ADD NEW RSS FEED'

        self.url = self.add(npyscreen.TitleText, name = "RSS URL:", value= "www.a_beautiful_rss.com" )
        self.name = self.add(npyscreen.TitleText, name = "NAME:", value= "Name to identify the rss-feed." )
        self.description = self.add(npyscreen.TitleText, name = "DESCRIPTION:", value= "Write a simple description about the origin of the RSS Feed." )
        self.date_added = self.add(npyscreen.TitleDateCombo, name='DATE ADDED', value= datetime.today(),editable=False)

    def on_ok(self):
        msg = """
RSS FEED TO BE ADDED\n
=========================\n
URL: {0} \n
DESCRIPTION: {1}\n
DATE ADDED: {2}\n
=========================\n
                """.format(
            str(self.url.value),
            str(self.description.value),
            str(self.date_added.value)
                )
        notify_result = npyscreen.notify_ok_cancel(msg, title= 'RSS TO BE SAVED')
        if(notify_result==True):
            npyscreen.notify_wait('SALIO SI')
            add_new_rss_feed({
                'url': self.url.value,
                'name': self.name.value,
                'desc': self.description.value,
                'created_date': self.date_added.value,
                'status': True,
                }
                )
            self.parentApp.switchForm('MAIN')
        else:
            npyscreen.notify_wait('SALIO NO')
            self.parentApp.switchForm('ADDFEED')

    def on_cancel(self):
        npyscreen.notify_wait('CANSEL SAVE!')
        self.parentApp.switchForm('MAIN')

