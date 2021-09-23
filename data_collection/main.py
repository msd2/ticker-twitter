from scrape_functions import *
from config import api_key, api_secret
from datetime import date
from google.cloud import storage
import pandas as pd

today = date.today()
today = today.strftime("%Y_%m_%d")

# Setup the bucket object with the google cloud credentials
bucket_name = 'uk-gov-tweets-14289'
storage_client = storage.Client.from_service_account_json('creds.json')
bucket = storage_client.get_bucket(bucket_name)

# Get the latest tweet id for each politician.
# This concatenates all csv files in the bucket.
latest_tweet = read_from_bucket(bucket=bucket)
latest_tweet = latest_tweet.groupby('user').max()['id']

# Authenticate with the twitter API.
api = authenticate(api_key, api_secret)

# Pull in the political twitter accounts.
# It does this from https://www.politics-social.com/api/list/csv/followers
politician_twitter_handles = return_politician_handles(option='list')

# Use tweepy and the twitter API to collect the political tweets.
data = tweet_grabber(politician_twitter_handles, api, 20)

# Create a temp csv which is used to upload to bucket.
data.to_csv('temp_data/tweets.csv', index=False)

# Upload the files to the bucket with the date in the name.
upload_to_bucket('tweets_'+today, 'temp_data/tweets.csv', bucket)


# Below code block for pulling tweets in batches.
# Potentially obselete.
"""
batchsize = 50
frames = []
for i in range(0, len(politician_twitter_handles), batchsize):
    batch = politician_twitter_handles[i:i+batchsize]
    data = tweet_grabber(batch, api, 20)
    frames.append(data)
data = pd.concat(frames)
"""
