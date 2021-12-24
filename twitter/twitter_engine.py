from configparser import ConfigParser

import tweepy

config = ConfigParser()

config.read('../config/main_config.ini')

auth = tweepy.OAuthHandler(config['twitter']['api_key'],
                           config['twitter']['api_secret_key'])
auth.set_access_token(config['twitter']['access_token'],
                      config['twitter']['access_token_secret'])

api = tweepy.API(auth)


class TwitterEngine:
    def __init__(self):
        self.api = self.connect_twitter()

    def connect_twitter(self):
        """Makes a connection to the twitter api for the class."""
        config = ConfigParser()
        config.read('../config/main_config.ini')
        auth = tweepy.OAuthHandler(config['twitter']['api_key'],
                                   config['twitter']['api_secret_key'])
        auth.set_access_token(config['twitter']['access_token'],
                              config['twitter']['access_token_secret'])
        api = tweepy.API(auth)
        return (api)

    def get_twitter_time_line(self):
        """ Returns my own timeline."""
        #  return api.home_timeline()
        time_line = api.home_timeline()
        return ([i._json for i in time_line])

    def update_status(self, text, tags, url):
        print('self')
        print('TEXT', text)
        print('TAGS', tags)
        print('URL', url)
