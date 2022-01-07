from configparser import ConfigParser
from pathlib import Path

import tweepy


class TwitterEngine:
    def __init__(self):
        """Makes a connection to the twitter api for the class."""
        config_file = Path(__file__).parent / "../config/main_config.ini"
        self.config = ConfigParser()
        self.config.read(config_file)
        auth = tweepy.OAuthHandler(self.config['twitter']['api_key'],
                                   self.config['twitter']['api_secret_key'])
        auth.set_access_token(self.config['twitter']['access_token'],
                              self.config['twitter']['access_token_secret'])
        self.api = tweepy.API(auth)

    def get_twitter_time_line(self):
        """ Returns my own timeline."""
        time_line = self.api.home_timeline()
        return ([i._json for i in time_line])

    def update_status(self, text):
        self.api.update_status(text)
