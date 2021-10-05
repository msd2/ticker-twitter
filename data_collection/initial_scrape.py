from scrape_functions import *
from config import api_key, api_secret
from datetime import datetime
from google.cloud import storage
import pandas as pd

date_time = datetime.now()
date_time = date_time.strftime('%Y_%m_%d, %H')

# Setup the bucket object with the google cloud credentials
bucket_name = 'uk-gov-tweets-14289'
storage_client = storage.Client.from_service_account_json('creds.json')
bucket = storage_client.get_bucket(bucket_name)

# Authenticate with the twitter API.
api = authenticate(api_key, api_secret)

names = read_from_bucket(bucket=bucket)
names = names['user']
names.drop_duplicates(inplace=True)

# Use tweepy and the twitter API to collect the political tweets.
data = initial_tweet_scrape(names, api, 30)


# Create a temp csv which is used to upload to bucket.
data.to_csv('temp_data/tweets.csv', index=False)


# Upload the files to the bucket with the date in the name.
upload_to_bucket('tweets_'+date_time, 'temp_data/tweets.csv', bucket)