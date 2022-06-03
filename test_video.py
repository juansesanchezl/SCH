import tweepy 
import webbrowser
import time
import json
import numpy as np
import requests
import base64
#https://iq.opengenus.org/post-video-twitter-api/
#pip install pandas --user
import pandas as pd
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

acc_token = access_token
acc_token_secret = access_token_secret
oAuthCredentials = {
  'consumer_key': consumer_key,
  'consumer_secret': consumer_secret,
  'token': acc_token,
  'token_secret': acc_token_secret
}

#callback_uri = 'oob'
#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token('1305341332102230018-cUk6dBETG134C1auClTx3JtSpkoCtH', 'jTyAuvWL0sqChAV3s5hsHQWwXDPquzSTV51faowfJU7dO')
#api = tweepy.API(auth, wait_on_rate_limit=True)


#Reformat the keys and encode them
key_secret = '{}:{}'.format(consumer_key, consumer_secret).encode('ascii')
#Transform from bytes to bytes that can be printed
b64_encoded_key = base64.b64encode(key_secret)
#Transform from bytes back into Unicode
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)
auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}
auth_data = {
    'grant_type': 'client_credentials'
}
auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
print(auth_resp.status_code)
access_token = auth_resp.json()['access_token']
print(access_token)

file = open('./videos/video2.mp4', 'rb')
data = file.read()
resource_url='https://upload.twitter.com/1.1/media/upload.json'
upload_video={
    'media':data,
    'media_category':'tweet_video'}
    
video_headers = {
    'Authorization': 'Bearer {}'.format(access_token)    
}

media_id=requests.post(resource_url,headers=video_headers,params=upload_video)
tweet_meta={ "media_id": media_id,
  # image alt text metadata
  "alt_text": {
    "text":"your_video_metadata_here" 
  }}
metadata_url = 'https://upload.twitter.com/1.1/media/metadata/create.json'    
metadata_resp = requests.post(metadata_url,params=tweet_meta,headers=auth_data)
print(metadata_resp.status_code)

tweet={'status':'hello world','media_ids':media_id}
post_url = 'https://api.twitter.com/1.1/statuses/update.json'    
post_resp = requests.post(post_url,params=tweet,headers=video_headers)
print(post_resp.status_code)

