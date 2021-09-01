import tweepy
from config import api_key, api_secret
import pandas as pd
from collections import defaultdict

def authenticate(api_key, api_secret):
    auth = tweepy.AppAuthHandler(api_key, api_secret)
    api = tweepy.API(auth)
    return api

def get_tweets(api, search, lang, items):
    d=defaultdict(list)
    q=search+'-filter:retweets'
    for tweet in tweepy.Cursor(api.search, q=q, lang=lang).items(items):
        d['tweet'].append(tweet.text)
        d['created'].append(tweet.created_at)
    df = pd.DataFrame(d)
    return df

