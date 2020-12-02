import tweepy
import time
import os
from hidden import *

class TweetMachine:
    def __init__(self):
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)
    
    def makeATweet(self,text):
        self.api.update_status(text)

    def makeAVidTweet(self,fileLoc,text):
        upload_result = self.api.media_upload(fileLoc)
        time.sleep(120)
        media_ids = [upload_result.media_id_string]
        self.api.update_status(status=text, media_ids=media_ids)
