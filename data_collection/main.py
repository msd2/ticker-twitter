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

# Authenticate with the twitter API.
api = authenticate(api_key, api_secret)


names_and_ids = read_from_bucket(bucket=bucket)
names_and_ids = names_and_ids.groupby('user').max()['id'].reset_index()

# # Use tweepy and the twitter API to collect the political tweets.
data = tweet_grabber(names_and_ids, api, 30)


# # Create a temp csv which is used to upload to bucket.
data.to_csv('temp_data/tweets.csv', index=False)


# # Upload the files to the bucket with the date in the name.
upload_to_bucket('tweets_'+today, 'temp_data/tweets.csv', bucket)
