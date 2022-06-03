
import tweepy 
import webbrowser
import time
import json
#pip install pandas --user
import pandas as pd
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

'''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)
'''
callback_uri = 'oob'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret,callback_uri)
redirect_url = auth.get_authorization_url()
#URL TO AUTHORIZE TWITTER APP
#print(redirect_url)
webbrowser.open(redirect_url)
user_pint_input = input("What's the pin value ? ")
#print(user_pint_input)
print(auth.get_access_token(user_pint_input))
#print(auth.access_token, access_token_secret)
api = tweepy.API(auth)
me = api.me()
#print(me.screen_name)
#WRITE A SIMPLE TWEET
#new_status = api.update_status("This is a test from python ")
#print(new_status)
#WRITE A TWEET WITH MEDIA
#IMAGE ID EXPIRES IN 20-24 hrs
#img_obj = api.media_upload("./images/clock.png")
#img_obj = api.media_upload("./images/modo_serio.jpg")
#print(img_obj)
#new_status = api.update_status("This is a test from python with media", media_ids=[img_obj.media_id_string])
#new_status = api.update_status("Cuando te toca mandar un tweet con imagen incluida por 2", media_ids=['1373809454077071361'])
#print(new_status)
def extract_timeline_as_df(timeline_list):
    columns = set()
    allowed_types = [str,int]
    tweets_data = []
    #my_timeline = api.home_timeline()
    for status in timeline_list:
        #print(status.text)
        status_dict = dict(vars(status))
        keys = status_dict.keys()
        #print(status.user)
        #print(status.author)
        single_tweet_data = {"user": status.user.screen_name, "author": status.author.screen_name}
        for k in keys:
            try:
                v_type = type(status_dict[k])
            except:
                v_type = None
            if v_type != None:
                if v_type in allowed_types:
                    single_tweet_data[k] = status_dict[k]
                    columns.add(k)
        tweets_data.append(single_tweet_data)
    header_cols = list(columns)
    header_cols.append("user")
    header_cols.append("author")
    df = pd.DataFrame(tweets_data,columns=header_cols)
    #df.head()
    return df

my_timeline = api.home_timeline()
df2 = extract_timeline_as_df(my_timeline)
print(df2.head())