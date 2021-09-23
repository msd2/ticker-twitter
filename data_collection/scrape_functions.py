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




def tweet_grabber(names_and_ids, api, number_of_tweets):
    d = defaultdict(list)
    print('\nScraping tweets...\n\n')
    for i, row in names_and_ids.iterrows():
        print(row['user']+':  '+str(i)+'/'+str(len(names_and_ids)))
        new_tweets = 0
        try:
            tweets = tweepy.Cursor(api.user_timeline, screen_name=row['user'], since_id=row['id']).items(number_of_tweets)
            for tweet in tweets:
                new_tweets+=1
                d['id'].append(tweet.id)
                d['text'].append(tweet.text)
                d['created'].append(tweet.created_at)
                d['user'].append(tweet.user.screen_name)
        except tweepy.error.TweepError:
            print("\n\nUser doesn't exist:\n\n"+row['user'])
            pass
        print(str(new_tweets)+' new tweets.\n')
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



def return_politician_handles(option='list'):
    req = Request('https://www.politics-social.com/api/list/csv/followers', headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    s=str(webpage,'utf-8')
    data = StringIO(s) 
    df=pd.read_csv(data)
    df['Name'] = df['Name'].apply(lambda x: x.rstrip())
    df['Screen name'] = df['Screen name'].apply(lambda x: x[1:])
    politician_handles = df['Screen name']
    print('Politician twitter handles imported.\n')

    if option=='list':
        return politician_handles
    else:
        return df