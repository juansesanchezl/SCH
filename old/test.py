from twython import Twython, TwythonError
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)
import json

twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

message = "This is a normal tweet"
twitter.update_status(status=message)
print("Tweeted: %s" % message)
