from scraper import authenticate, tweet_grabber, upload_to_bucket
from config import api_key, api_secret

api = authenticate(api_key, api_secret)
data = tweet_grabber('government_twitter_handles.txt', api, 5)
data.to_csv('temp_data/tweets.csv', index=False)
upload_to_bucket('tweets', 'temp_data/tweets.csv', 'uk-gov-tweets-14289')