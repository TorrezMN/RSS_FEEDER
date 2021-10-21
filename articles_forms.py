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


class UpdateArticlesDB(npyscreen.Popup):

    def create(self):
        self.name='UPDATE ARTICLES DB'
        self.feeds = get_all_rss_feeds()
        
        self.slider = self.add(
            npyscreen.TitleSlider, 
            out_of=len(self.feeds), 
            step=1,
            label=True, 
            color='LABEL',
            name='UPDATING NEWS!')

        self.keypress_timeout = 15

    def while_waiting(self):
        curses.beep()
        npyscreen.blank_terminal()
        if(self.slider.value<len(self.feeds)):
            npyscreen.notify_wait(
                'FEED URL: {0} \nFEED NAME: {1}'.format(
                    self.feeds[int(self.slider.value)].url,
                    self.feeds[int(self.slider.value)].name),
                title='UPDATING NOW'
                )
            get_news_feeds(
                self.feeds[int(self.slider.value)].url,
                self.feeds[int(self.slider.value)]
                )    
            npyscreen.blank_terminal()
        
        try:
            self.slider.value +=1
        except ValueError:
            npyscreen.notify_wait('NEWS UPDATE FINISH!', title='FINISH UPDATE')
            self.parentApp.switchForm('MAIN')


    def afterEditing(self):
        self.parentApp.switchForm('MAIN')

class SearchArticles(npyscreen.ActionForm, npyscreen.FormBaseNew):
    def create(self):
        self.name='SEARCH ARTICLES'
        self.search_term = self.add(npyscreen.TitleText, name = "SEARCH TERMS:", value= "sample term")
        
    

    def pre_edit_loop(self):
        cls()

    

    def afterEditing(self):
        npyscreen.notify_confirm('TERM TO SEARCH: {0}'.format(self.search_term.value))
        self.parentApp.switchForm('MAIN')

class ListArticles(npyscreen.Form):

    OK_BUTTON_TEXT = 'ACEPTAR'
    
    def create(self):
        self.name='LIST OF ARTICLE'
        self.news_list = [i.title for i in get_list_articles()]
        self.title = self.add(npyscreen.TitleText, name = "TOTAL:", value= "{0}".format(len(get_list_articles())) , editable = False)
        self.options_selected = self.add(npyscreen.TitleSelectOne, name='NEWS LIST', values = self.news_list)
        self.keypress_timeout = 10
        self.engine = pyttsx3.init()
        self.newVoiceRate = 145
        
    def while_waiting(self):
        if(len(self.options_selected.value)>0 and self.parentApp.read):
            self.engine.setProperty('rate',self.parentApp.voice_rate)
            self.engine.setProperty('volume',self.parentApp.systemVolume)  
            self.engine.say(self.news_list[self.options_selected.value[0]])
            self.engine.runAndWait()
        else:
            if(self.parentApp.read):
                npyscreen.notify_confirm('YOU CAN SELECT AN ARTICLE AND WILL BE READED AUT LOUD!')
            else:
                pass

    def afterEditing(self):
        publish = npyscreen.notify_ok_cancel('AFTER EDIT ON LIST OF ARTICLES : \n {0}'.format(self.news_list[self.options_selected.value[0]]))
        npyscreen.notify_wait('publish {0}'.format(publish))
        npyscreen.blank_terminal()

        publ = self.parentApp.getForm("PUBLISHARTICLE")
        publ.title.value = self.news_list[self.options_selected.value[0]]
        publ.author.value = 'some great author'
        publ.tags.value = 'teast, asdflasdf, tas , atatsda'
        self.parentApp.switchForm("PUBLISHARTICLE")
        


class PublishArticle(npyscreen.Form):

    OK_BUTTON_TEXT = 'PUBLISH NOW'

    def create(self):
        self.name='PUBLISH ARTICLE'
        self.title = self.add(npyscreen.TitleText, name = "TITLE:", value= "Sample text." , editable = False)
        self.author = self.add(npyscreen.TitleText, name = "AUTHOR:", value= "Sample text." , editable = False)
        self.tags = self.add(npyscreen.TitleText, name = "TAGS:", value= "Sample text." , editable = False)
        self.nextrely += 2

        self.add(npyscreen.ButtonPress, name="Cerrar sesión", when_pressed_function=self.close_session)
        

    def close_session(self):
        npyscreen.notify_confirm('COSING SESSION{0}'.format(dir(self)))
    def afterEditing(self):
        self.parentApp.switchForm('MAIN')


