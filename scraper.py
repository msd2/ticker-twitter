import tweepy
from config import api_key, api_secret
import pandas as pd
from collections import defaultdict
import re
from textblob import TextBlob

class TweetCollector:

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.auth = tweepy.AppAuthHandler(self.api_key, self.api_secret)
        self.api = tweepy.API(self.auth)
    
    def deEmojify(self, text):
        regrex_pattern = re.compile(pattern = "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags = re.UNICODE)
        return regrex_pattern.sub(r'',text)

    def clean(self, tweet):
        tweet = tweet.strip(' ')
        tweet = self.deEmojify(tweet)
        tweet = re.sub(r'^RT[\s]+', '', tweet)
        tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
        tweet = re.sub(r'#', '', tweet)
        tweet = re.sub(r'@[A-Za-z0–9]+', '', tweet) 
        tweet = re.sub(r'\n','', tweet)
        return tweet
    
    def get_tweets(self, search, lang, items):
        d=defaultdict(list)
        q=search+'-filter:retweets'
        for tweet in tweepy.Cursor(self.api.search, q=q, lang=lang).items(items):
            d['tweet'].append(tweet.text)
            d['created'].append(tweet.created_at)
            d['id'].append(tweet.id)
        df = pd.DataFrame(d)
        df['tweet'] = df['tweet'].apply(self.clean)
        return df