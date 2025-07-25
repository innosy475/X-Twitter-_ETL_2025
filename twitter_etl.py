import tweepy
import pandas as pd
import json
from datetime import datetime
import s3fs

access_key = "ZqWhiTo2RsKonlLKRr2x3yj1P"
access_secret = "lvQDIjLvVmLULsSlGk4EHnH2mBQUOAPauzmDQ1B4WkrECgCjAS"
consumer_key = "3694029853-dpZVsosTV6ceOqUnwcwX2IAYocCh6XlZ0UzsdeJ"
consumer_secret = "VvyRzc01i6EvuHq2WAP9dCkXfVL17OwpBCsHaAuTurj3L"


# Twitter authentication
auth = tweepy.OAuthHandler(access_key, access_secret)
auth.set_access_token(consumer_key, consumer_secret)

# Creating an API object
api = tweepy.API(auth)

tweets = api.user_timeline(screen_name='@elonmusk',
                          # 200 is the maximum allowed count
                          count=200,
                          include_rts=False,
                          # Necessary to keep full text
                          # otherwise only the first 140 words are extracted
                          tweet_mode='extended'
                          )