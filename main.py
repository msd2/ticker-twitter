from scraper import TweetCollector
from config import api_key, api_secret
import tweepy

tweets = TweetCollector(api_key, api_secret)
data = tweets.get_tweets('#ETH','en',2000)
data = tweets.find_sentiment(data)
data.to_csv('tweet_data.csv', index=False)
auth = tweepy.AppAuthHandler(api_key, api_secret)