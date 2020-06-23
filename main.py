import tweepy
import requests
import sys
from datetime import timedelta
import MyAPI
import reply
import traceback

class Listener(tweepy.StreamListener):
    def on_status(self, status):
        status.created_at += timedelta(hours=9)
        print('------------------------------')
        print(status.text)
        print("{name}({screen}) {created} via {src}\n".format(name=status.author.name, screen=status.author.screen_name,created=status.created_at, src=status.source))
        if ("RT @" not in status.text) and (not "https:" in status.text):
            reply.reply(status.text, status.user.name, status.id,status.author.screen_name, status.retweeted)
        return True

    def on_error(self, status_code):
        print('error: ' + str(status_code))
        return True

    def on_timeout(self):
        print('Timeout...')
        return True

authR = tweepy.OAuthHandler(MyAPI.consumer_key_read, MyAPI.consumer_secret_read)
authR.set_access_token(MyAPI.access_token_read, MyAPI.access_secret_read)

listener = Listener()

stream = tweepy.Stream(authR, listener)
while True:
    try:
        stream.filter(track=["#お願いチュウニペンギン"])
    except KeyboardInterrupt:
        print("\nkeyboardInterrupt\n")
        sys.exit()
    except:
        traceback.print_exc()
