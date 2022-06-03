
#https://docs.tweepy.org/en/latest/index.html
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
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
#redirect_url = auth.get_authorization_url()
#URL TO AUTHORIZE TWITTER APP
#print(redirect_url)
#webbrowser.open(redirect_url)
#user_pint_input = input("What's the pin value ? ")
#print(user_pint_input)
#print(auth.get_access_token(user_pint_input))
#print(auth.access_token, access_token_secret)

#api = tweepy.API(auth)
#me = api.me()

#print(me.screen_name)
#WRITE A SIMPLE TWEET
#new_status = api.update_status("This is a test from python ")
#print(new_status)
#WRITE A TWEET WITH MEDIA
#IMAGE ID EXPIRES IN 20-24 hrs
#img_obj = api.media_upload("./images/clock.png")
#JPG
print('JPG')
img_obj = api.media_upload("./images/modo_serio.jpg")
print(img_obj)
new_status = api.update_status("This is a test from python with media (jpg)", media_ids=[img_obj.media_id_string])
print(new_status)
time.sleep(2)
print('PNG')
#PNG
img_obj = api.media_upload("./images/meme.png")
print(img_obj)
new_status = api.update_status("This is a test from python with media (png)", media_ids=[img_obj.media_id_string])
print(new_status)
time.sleep(2)
print('GIF')
#GIF
img_obj = api.media_upload("./images/memes-dream.gif")
print(img_obj)
new_status = api.update_status("This is a test from python with media (GIF)", media_ids=[img_obj.media_id_string])
print(new_status)
time.sleep(2)






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
'''
my_timeline = api.home_timeline()
df2 = extract_timeline_as_df(my_timeline)
print(df2.head())
'''
#user = api.get_user("gisselleapa")
# GET LAST TWEET OF USER, LIKE , RT AND REPLY IT
'''
user_timeline = user.timeline()
user_timeline_status_obj = user_timeline[0]
status_obj_id = user_timeline_status_obj.id
status_obj_screen_name = user_timeline_status_obj.user.screen_name
status_obj_url = f"https://twitter.com/{status_obj_screen_name}/status/{status_obj_id}"
print(status_obj_url)
api.retweet(status_obj_id)
api.create_favorite(status_obj_id)
#api.destroy_favorite(status_obj_id)
og_tweet = api.get_status(status_obj_id)
my_reply = api.update_status(f"@{og_tweet.user.screen_name} jajajaja", og_tweet.id)
'''

#GET FOLLOWERS FROM ANOTHER USER AND FOLLOW THEM AND UNFOLLOW THEM
'''
my_new_friends = []
user_friends = user.friends()
for friend in user_friends:
    if friend.followers_count > 300 and friend.friends_count < 300:
        print(friend.screen_name)
        my_new_friends.append(friend.screen_name)
        relationship_ = api.create_friendship(friend.screen_name)
        #api.create_friendship(friend.screen_name)

print(my_new_friends)
to_remove = my_new_friends
for username in to_remove:
    api.destroy_friendship(username)
'''



#for i, status in enumerate(tweepy.Cursor(api.home_timeline).items(50)):
#    print(i, status.text)

other_user = '_modosocial'
#USER TIMELINE
#for i, status in enumerate(tweepy.Cursor(api.user_timeline, screen_name=other_user).items(20)):
#    print(i,status.text)

#GET USER FRIENDS IDs
'''
the_social_friends = []
for i, _id in enumerate(tweepy.Cursor(api.friends_ids, screen_name = other_user).items(30)):
    #print(i, _id)
    the_social_friends.append(_id)
    
for id in the_social_friends:
    print(api.get_user(id).screen_name)
'''

#GET TWEETS BY QERY PARAMETERS
'''
query = "#Millonarios -Vladimir -VAR"
for i, status in enumerate(tweepy.Cursor(api.search, q=query).items(10)):
    print(i, status.text, status.author.screen_name)
'''
#GET USERS BY NAME
'''
query_username = "Millonarios"
for i, user in enumerate(tweepy.Cursor(api.search_users, q=query, per_page=20).items(10)):
    print(i, user.screen_name)
'''

#GET DISTINCT USERS AND ADD THEM IN A SET
'''
query_username = "Millonarios"
search_results = set()
for i, user in enumerate(tweepy.Cursor(api.search_users, q=query_username).items(50)):
    #print(i, user.screen_name)
    search_results.add(user.screen_name)
print(list(search_results))
'''

#HANDLE WHEN TWEEPY CAME TO RATELIMTERROR 15 MIN, AND SLEEP IT
'''
query_username = "Millonarios"
def process_page(page_results):
    for i, user in enumerate(page_results):
        print(i, user.screen_name)


for i, page in enumerate(tweepy.Cursor(api.search_users, q=query_username, per_page=10).pages(3)):
    print(i, "page------------")
    process_page(page)

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            #SEND EMAIL / WEBHOOK
            time.sleep(15 * 60) #15 minutes

for follower in limit_handled(tweepy.Cursor(api.followers).items()):
    print(follower.screen_name)
'''