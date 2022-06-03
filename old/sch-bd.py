from twython import Twython
import json

CREDS_FILENAME = 'creds.json'

with open(CREDS_FILENAME, 'r') as f:
    creds = json.load(f)

tempclient = Twython(creds['consumer_key'], creds['consumer_secret'])
tcreds = tempclient.get_authentication_tokens()
authclient = Twython(creds['consumer_key'], creds['consumer_secret'],
                    tcreds['oauth_token'],
                    tcreds['oauth_token_secret'])

print(tcreds['auth_url'])
'''
##################################
# MANUAL STEP
# visit that page in your browser
# ...hit the button to "Authorize app"
# ...then copy and paste the pin number into your code

the_pin_number = 1234567

## END MANUAL STEP
##################################

realcreds = authclient.get_authorized_tokens(the_pin_number)
# Create a client that acts on behalf of your secondary user
second_user = Twython(creds['consumer_key'], creds['consumer_secret'],
                        realcreds['oauth_token'],
                        realcreds['oauth_token_secret'])

# Check its read-access
second_user.get_account_settings()

# Check its write-access
second_user.update_status(status='hello world for the second time')
'''