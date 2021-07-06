import tweepy
from config import api_key, api_secret

auth = tweepy.AppAuthHandler(api_key, api_secret)
api = tweepy.API(auth)


for tweet in tweepy.Cursor(api.search, q='#ETH', lang='en').items(100):
    print(tweet.text)
    print('\n')