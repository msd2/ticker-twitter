from scrape_functions import authenticate, return_politician_handles, tweet_grabber, upload_to_bucket
from config import api_key, api_secret
from datetime import date
from google.cloud import storage
import pandas as pd

today = date.today()
today = today.strftime("%Y_%m_%d")

api = authenticate(api_key, api_secret)
politician_twitter_handles = return_politician_handles()
batchsize = 50

storage_client = storage.Client.from_service_account_json(
        'creds.json')

frames = []
for i in range(0, len(politician_twitter_handles), batchsize):
    batch = politician_twitter_handles[i:i+batchsize]
    data = tweet_grabber(batch, api, 20)
    frames.append(data)

data = pd.concat(frames)
print(data)
data.to_csv('temp_data/tweets.csv', index=False)
upload_to_bucket('tweets_'+today, 'temp_data/tweets.csv', 'uk-gov-tweets-14289')