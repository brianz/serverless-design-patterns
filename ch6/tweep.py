import os
import tweepy
from pprint import pprint as pp

consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']

access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_token_secret = os.environ['TWITTER_ACCESS_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        #print(status.coordinates, status.source)
        print('*' * 100)
        print(status.text)
        media = status._json.get('entities', {}).get('media')
        if not media:
            print('passing')
            print
            return

        for m in media:
            if m['type'] != 'photo':
                continue
            print(m['media_url'])
        print


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
try:
    #myStream.filter(track=['realDonaldTrump'])
    myStream.filter(track=['#dog', '#dogs', '#puppy'])
except:
    #myStream.close()
    pass
