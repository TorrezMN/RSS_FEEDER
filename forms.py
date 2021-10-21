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





class ConfigSound(npyscreen.FormBaseNew, npyscreen.Popup):
        
    def create(self):
        self.name = 'SYSTEM VOLUME'
        
        self.read_stuff = self.add(
            npyscreen.Checkbox,
            name='READ SHIT'
            )

        self.actualVolume = self.add(
            npyscreen.TitleText, 
            name = "ACT VOLUME:", 
            value= "0" , 
            editable = False)

        self.slider = self.add(
            npyscreen.TitleSlider, 
            out_of=10, 
            step=.5,
            label=True, 
            color='LABEL',
            name='NEW VOLUME')
        self.voice_rate = self.add(
                npyscreen.TitleSlider,
                out_of=50,
                step=.5,
                label=True,
                color='LABEL',
                name='VOICE RATE'
                ) 
        
        self.nextrely+=2
        self.nextrelx+=40
        self.add(npyscreen.ButtonPress, name="CONFIRM", when_pressed_function=self.change_sound_volume)
                
        self.keypress_timeout = 10
        self.engine = pyttsx3.init()
 
    def change_sound_volume(self):
        self.parentApp.read = self.read_stuff.value
        self.parentApp.voice_rate = self.voice_rate.value
        self.parentApp.switchForm('MAIN')  

    def while_waiting(self):
        self.parentApp.systemVolume = self.slider.value
        self.parentApp.voice_rate = self.voice_rate.value
        curses.beep()
    
    def pre_edit_loop(self):
        cls()

        self.actualVolume.value = str(self.parentApp.systemVolume)
        

        



    def post_edit_loop(self):
        self.engine.setProperty('volume',self.parentApp.systemVolume)


