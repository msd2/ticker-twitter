import tweepy
from config import *
import json
import pandas as pd
from collections import defaultdict


class Listener(tweepy.StreamListener):

    def _init__(self):
        self.output = defaultdict(list)

    def on_data(self, raw_data):
        self.process_data(raw_data)
        return True

    def process_data(self, raw_data):
        raw_data = json.loads(raw_data)
        for key in raw_data.keys():
            self.output[key].append(raw_data[key])
        #print(raw_data.screen_name)

    def on_error(self, status_code):
        if status_code == 420:
            return False

class Stream():

    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(auth=auth, listener=listener)

    def start(self, keyword_list, to_follow):
        self.stream.filter(track=keyword_list, follow=to_follow, filter_level=None, languages=['en'])


if __name__ == '__main__':
    listener = Listener()
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)
    stream.start(['#ETH'],['2433432126'])