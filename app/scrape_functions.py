import tweepy
import pandas as pd
from collections import defaultdict
from urllib.request import Request, urlopen
from io import StringIO, BytesIO



def authenticate(api_key, api_secret):
    auth = tweepy.AppAuthHandler(api_key, api_secret)
    api = tweepy.API(auth)
    print('Twitter authentication successful.\n')
    return api



def read_from_bucket(bucket):
    frames = []
    files  = list(bucket.list_blobs())
    for file in files:
        blob = bucket.blob(file.name)
        data = pd.read_csv(BytesIO(blob.download_as_string()), encoding='utf-8')
        frames.append(data)
    data = pd.concat(frames)
    return data




def tweet_grabber(twitter_handles, api, number_of_tweets, since_id):
    d = defaultdict(list)
    print('Scraping tweets. Handle:')
    for user in twitter_handles:
        print(user)
        try:
            for tweet in tweepy.Cursor(api.user_timeline, screen_name=user, since_id=since_id).items(number_of_tweets):
                d['id'].append(tweet.id)
                d['text'].append(tweet.text)
                d['created'].append(tweet.created_at)
                d['user'].append(tweet.user.name)
        except tweepy.error.TweepError:
            print("user doesn't exist")
            pass
    tweets = pd.DataFrame(d)
    print('Tweets scraped.\n')
    return tweets



def upload_to_bucket(blob_name, source_file_name, bucket):
    print('Uploading to bucket.')
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(source_file_name)
    print(
        "File {} uploaded to {}.".format(
            source_file_name, blob_name
        )
    )



def return_politician_handles():
    req = Request('https://www.politics-social.com/api/list/csv/followers', headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    s=str(webpage,'utf-8')
    data = StringIO(s) 
    df=pd.read_csv(data)
    politician_handles = df['Screen name'].apply(lambda x: x[1:])
    print('Politician twitter handles imported.\n')
    return politician_handles