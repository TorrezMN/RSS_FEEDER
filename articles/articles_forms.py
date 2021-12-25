import curses
import itertools

import npyscreen

from db.db_engine import News, RSS_Feed
from db.db_toolkit import (add_news, filter_news_title, get_all_rss_feeds,
                           get_list_articles, delete_news)
from utils.utilities import get_news_from_rss, get_news_stats

from twitter.twitter_engine import TwitterEngine


def cls():
    npyscreen.blank_terminal()


class UPDATE_NEWS(npyscreen.FormBaseNew):
    def create(self):
        self.keypress_timeout = 10
        self.screen_size = self.curses_pad.getmaxyx()  #(height,width)
        self.rss_list = self.add(npyscreen.MultiLine,
                                 name='RSS FEEDS AVIALABLE',
                                 values=[i.url for i in get_all_rss_feeds()],
                                 max_height=int(self.screen_size[0] * 0.3),
                                 value=0,
                                 color='GOOD')

        #self.rss_list.when_check_cursor_moved = curses.beep
        self.rss_list.when_value_changed = curses.beep

    def while_waiting(self):
        #npyscreen.notify_ok_cancel('AWAIT! {0}'.format(get_news_from_rss(get_all_rss_feeds()[0])))
        try:
            cls()
            npyscreen.notify_wait('RSS URL :  {0}'.format(
                self.rss_list.values[self.rss_list.value]),
                                  title='UPDATING')

            for i in get_news_from_rss(RSS_Feed.select().where(
                    RSS_Feed.url == self.rss_list.values[
                        self.rss_list.value])):
                add_news(i)

            self.rss_list.value += 1
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
        self.screen_size = self.curses_pad.getmaxyx()  #(height,width)
        self.articles_list = [i.title for i in get_list_articles()]

        self.rss_list = self.add(npyscreen.MultiLine,
                                 name='RSS FEEDS AVIALABLE',
                                 values=self.articles_list,
                                 max_height=int(self.screen_size[0] * 0.45),
                                 value=0,
                                 color='GOOD')

        self.nextrely += 1
        self.draw_vertline_at = self.get_half_way() + 10
        self.nextrely += 1

        self.article_name = self.add(npyscreen.TitleText,
                                     name="NAME:",
                                     value="Name to identify the rss-feed.",
                                     editable=False,
                                     hidden=True)
        self.article_author = self.add(npyscreen.TitleText,
                                       name="AUTHOR:",
                                       value="Name to identify the rss-feed.",
                                       editable=False,
                                       hidden=True)
        self.article_publisher = self.add(
            npyscreen.TitleText,
            name="PUBLISHER:",
            value="Name to identify the rss-feed.",
            editable=False,
            hidden=True)

        self.nextrely += 1

        self.article_detail_btn = self.add(
            npyscreen.ButtonPress,
            name='DETAILS',
            when_pressed_function=self.article_detail,
            hidden=True,
            relx=int(self.screen_size[1] * 0.1),
            rely=int(self.screen_size[0] * 0.9))

        self.go_back_btn = self.add(npyscreen.ButtonPress,
                                    name='GO BACK',
                                    when_pressed_function=self.go_back,
                                    hidden=True,
                                    relx=int(self.screen_size[1] * 0.3),
                                    rely=int(self.screen_size[0] * 0.9))

        self.rss_list.when_check_cursor_moved = curses.beep
        self.rss_list.when_check_value_changed = self.new_value

    def pre_edit_loop(self):
        npyscreen.notify_wait('PRE EDIT LOOP LIST NEWS!')
        self.articles_list = [i.title for i in get_list_articles()]

    def article_detail(self):
        next_form = self.parentApp.getForm('DETAIL_NEWS')
        next_form.article_title.value = self.article_name.value
        self.parentApp.switchForm('DETAIL_NEWS')

    def go_back(self):
        self.parentApp.switchForm('MAIN')

    def new_value(self):
        try:
            art = News.select().where(
                News.title == self.rss_list.values[self.rss_list.value])

            self.article_name.value = art[0].title
            self.article_name.hidden = False

            self.article_author.value = art[0].author
            self.article_author.hidden = False

            self.article_publisher.value = RSS_Feed.select().where(
                RSS_Feed.id == art[0].feed)[0].name
            self.article_publisher.hidden = False

            self.article_detail_btn.hidden = False
            self.go_back_btn.hidden = False

            self.DISPLAY()
        except:
            self.DISPLAY()


class DETAIL_NEWS(npyscreen.FormBaseNew):
    def create(self):
        self.screen_size = self.curses_pad.getmaxyx()  #(height,width)
        self.article_title = self.add(npyscreen.TitleText,
                                      name='Article',
                                      editable=False)
        self.article_author = self.add(npyscreen.TitleText,
                                       name='Author',
                                       editable=False)
        self.article_publisher = self.add(npyscreen.TitleText,
                                          name='Publisher',
                                          editable=False)
        self.article_url = self.add(npyscreen.TitleText, hidden=True)
        self.article_tags = self.add(
            npyscreen.TitleMultiSelect,
            name='SUGESTED ARTICLE TAGS',
            #values = [],
            max_height=int(self.screen_size[0] * 0.5),
            value=0,
            color='GOOD')

        self.article_publish_btn = self.add(
            npyscreen.ButtonPress,
            name='PUBLISH',
            when_pressed_function=self.publish_article,
            hidden=True,
            relx=int(self.screen_size[1] * 0.1),
            rely=int(self.screen_size[0] * 0.9))
        self.article_go_back_btn = self.add(
            npyscreen.ButtonPress,
            name='GO BACK',
            when_pressed_function=self.go_back,
            hidden=True,
            relx=int(self.screen_size[1] * 0.3),
            rely=int(self.screen_size[0] * 0.9))

    def publish_article(self):
        cls()
        curses.beep
        selected = self.article_tags.get_selected_objects()
        tags = []
        for i in selected:
            if '#' in i:
                for j in i.split('#'):
                    if (len(j) > 1):
                        tags.append(str(j))
            else:
                tags.append(str(i))
        # Removing duplicated tags.
        tags = list(set(tags))

        cls()
        to_publish = npyscreen.notify_ok_cancel(
            'ARTICLE: {0} \n\nSUGGESTED TAGS: {1}\n\n URL:{2}'.format(
                self.article_title.value, tags, self.article_url.value))

        if (to_publish):
            te = TwitterEngine()
            npyscreen.notify_wait('TWITTER TIMELINE  : \n\n {0}'.format(
                te.get_twitter_time_line()))

            # Delete news.
            npyscreen.notify_wait('ARTICLE TITLE {0}'.format(
                self.article_title.value))
            delete_news(self.article_title.value)
            self.parentApp.switchForm('MAIN')
        else:
            self.parentApp.switchForm('MAIN')
        cls()

    def go_back(self):
        self.parentApp.switchForm('LIST_NEWS')

    def pre_edit_loop(self):
        curses.beep
        art = News.select().where(News.title == self.article_title.value)
        self.article_title.value = art[0].title
        self.article_author.value = art[0].author
        self.article_publisher.value = RSS_Feed.select().where(
            RSS_Feed.id == art[0].feed)[0].name
        self.article_url.value = art[0].link_url
        self.article_tags.values = [
            tag[1] for tag in get_news_stats(art[0].link_url)['tags']
        ]

        self.article_publish_btn.hidden = False
        self.article_go_back_btn.hidden = False


class SEARCH_NEWS(npyscreen.FormBaseNew):
    def create(self):
        self.screen_size = self.curses_pad.getmaxyx()  #(height,width)
        self.article_title = self.add(
            npyscreen.TitleText,
            name='SEARCH',
            value_changed_callback=self.the_value_has_changed,
        )

        self.new_val = self.add(npyscreen.TitleText, name='NEW VALUE')

    def the_value_has_changed(self, a):
        cls()
        if (not isinstance(self.article_title.value, None)):
            npyscreen.notify_ok_cancel('CURRENT VALUE {0}{1}'.format(
                self.article_title.value, a))
        self.DISPLAY()

    def pre_edit_loop(self):
        npyscreen.notify_ok_cancel('{0}\n\n\n\n{1}'.format(
            dir(self.article_title),
            self.article_title.value_changed_callback))
