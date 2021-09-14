import tweepy
import pandas as pd
from collections import defaultdict
from google.cloud import storage

def authenticate(api_key, api_secret):
    auth = tweepy.AppAuthHandler(api_key, api_secret)
    api = tweepy.API(auth)
    return api

def tweet_grabber(twitter_handles, api, number_of_tweets):
    d = defaultdict(list)
    with open(twitter_handles, "r") as handles:
        for user in handles:
            for tweet in tweepy.Cursor(api.user_timeline, screen_name=user).items(number_of_tweets):
                d['text'].append(tweet.text)
                d['created'].append(tweet.created_at)
                d['user'].append(tweet.user.name)
    tweets = pd.DataFrame(d)
    return tweets

def upload_to_bucket(blob_name, source_file_name, bucket_name):
    """ Upload data to a bucket"""

    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json(
        'twitter-325919-9d64dbc990f3.json')

    #print(buckets = list(storage_client.list_buckets())

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, blob_name
        )
    )
