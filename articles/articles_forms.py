import curses
import npyscreen
from db.db_toolkit import get_all_rss_feeds
from db.db_toolkit import get_list_articles
from db.db_toolkit import add_news
from db.db_engine import RSS_Feed
from db.db_engine import News
from utils.utilities import get_news_from_rss
from utils.utilities import get_news_stats
 
class UPDATE_NEWS(npyscreen.FormBaseNew):

    def create(self):
        self.keypress_timeout = 10
        self.screen_size = self.curses_pad.getmaxyx() #(height,width)
        self.rss_list = self.add(
                npyscreen.MultiLine,
                name='RSS FEEDS AVIALABLE',
                values = [i.url for i in get_all_rss_feeds()],
                max_height= int(self.screen_size[0]*0.3),
                value = 0,
                color='GOOD'
                )

        #self.rss_list.when_check_cursor_moved = curses.beep
        self.rss_list.when_value_changed = curses.beep
    

    def while_waiting(self):
        #npyscreen.notify_ok_cancel('AWAIT! {0}'.format(get_news_from_rss(get_all_rss_feeds()[0])))
        try:
            npyscreen.notify_wait('RSS URL :  {0}'.format(self.rss_list.values[self.rss_list.value]), title='UPDATING')
            #npyscreen.notify_ok_cancel('FEDD {0}'.format(
            #    RSS_Feed.select().where(RSS_Feed.url ==self.rss_list.values[self.rss_list.value])
            #    ))
          
            for i in get_news_from_rss(RSS_Feed.select().where(RSS_Feed.url ==self.rss_list.values[self.rss_list.value])):
                add_news(i)


            self.rss_list.value +=1
            self.DISPLAY()
        except IndexError:
            npyscreen.notify_wait('FINISH UPDATING RSS NEWS', title='UPDATING')
            self.parentApp.switchForm('MAIN')
            self.DISPLAY()

class LIST_NEWS(npyscreen.FormBaseNew, npyscreen.SplitForm):

    MOVE_LINE_ON_RESIZE = True

    def create(self):
        #self.keypress_timeout = 10
        self.name = "LIST NEWS | TOTAL: {0}".format(len(get_list_articles()))
        self.screen_size = self.curses_pad.getmaxyx() #(height,width)
        self.rss_list = self.add(
                npyscreen.MultiLine,
                name='RSS FEEDS AVIALABLE',
                values = [i.title for i in get_list_articles()],
                max_height= int(self.screen_size[0]*0.45),
                value = 0,
                color='GOOD'
                )
        
        self.nextrely += 1
        self.draw_vertline_at = self.get_half_way()+10
        self.nextrely += 1

        self.article_name = self.add(
            npyscreen.TitleText, 
            name = "NAME:", 
            value= "Name to identify the rss-feed.",
            editable=False,
            hidden=True
            )
        self.article_author = self.add(
            npyscreen.TitleText, 
            name = "AUTHOR:", 
            value= "Name to identify the rss-feed.",
            editable=False,
            hidden=True
            )
        self.article_publisher = self.add(
            npyscreen.TitleText, 
            name = "PUBLISHER:", 
            value= "Name to identify the rss-feed.",
            editable=False,
            hidden=True
            )
        

        self.nextrely += 1

        self.article_detail_btn = self.add(
            npyscreen.ButtonPress,
            name='DETAILS',
            when_pressed_function=self.article_detail, 
            hidden=True,
            relx=int(self.screen_size[1]*0.1),
            rely = int(self.screen_size[0]*0.9)
            )

        self.go_back_btn = self.add(
            npyscreen.ButtonPress,
            name='GO BACK',
            when_pressed_function=self.go_back, 
            hidden=True,
            relx=int(self.screen_size[1]*0.2),
            rely = int(self.screen_size[0]*0.9)
            )

        self.rss_list.when_check_cursor_moved = curses.beep
        self.rss_list.when_check_value_changed = self.new_value
        

    def article_detail(self):
        next_form = self.parentApp.getForm('DETAIL_NEWS')
        next_form.article_title.value = self.article_name.value
        self.parentApp.switchForm('DETAIL_NEWS')


    def go_back(self):
        self.parentApp.switchForm('MAIN')

    
    def new_value(self):
        try:
            art =  News.select().where(News.title == self.rss_list.values[self.rss_list.value])        
            
            self.article_name.value =art[0].title
            self.article_name.hidden = False
            
            self.article_author.value = art[0].author
            self.article_author.hidden = False
            
            self.article_publisher.value = RSS_Feed.select().where(RSS_Feed.id ==art[0].feed)[0].name
            self.article_publisher.hidden = False




            self.article_detail_btn.hidden = False
            self.go_back_btn.hidden = False

            self.DISPLAY()
        except:
            
            self.DISPLAY()



class DETAIL_NEWS(npyscreen.FormBaseNew):
    def create(self):
        self.article_title = self.add(npyscreen.TitleText, name='Article')
        self.article_author = self.add(npyscreen.TitleText, name='Author')
        self.article_publisher = self.add(npyscreen.TitleText, name='Publisher')
        self.article_url = self.add(npyscreen.TitleText, hidden=True)


    def pre_edit_loop(self):
        curses.beep
        art =  News.select().where(News.title == self.article_title.value)
        self.article_title.value = art[0].title
        self.article_author.value = art[0].author
        self.article_publisher.value = RSS_Feed.select().where(RSS_Feed.id ==art[0].feed)[0].name
        self.article_url.value = art[0].link_url
        npyscreen.notify_ok_cancel('COMMON WORDS: {0}'.format(get_news_stats(art[0].link_url)))
