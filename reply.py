import tweepy
import requests
import sys
import random
import MyAPI
import traceback

auth = tweepy.OAuthHandler(MyAPI.consumer_key_send, MyAPI.consumer_secret_send)
auth.set_access_token(MyAPI.access_token_send, MyAPI.access_secret_send)
api = tweepy.API(auth)

def serch_level(text):
    for i in range(100, 142):
        if (str(i / 10) in text) and (str(i / 10)[-1] != "0"):
            return str(i / 10)
        elif str(i / 10) in text:
            return str(int(i / 10))
    for i in range(10, 14):
        if (str(i) + "+" in text) or (str(i) + "＋" in text):
            return str(i)
        elif str(i) in text:
            return str(i)
    return "ALL"

# def serch_genre(text):
#     genre_list = []
#     ジャンルの指定をつくる

def reply(tw_text, tw_user_name, tw_id, tw_author_screen_name, tw_retweeted):
    level = serch_level(tw_text)
    file = open("Lv" + level + ".txt")
    song_list = file.readlines()
    file.close()
    selected_song = random.choice(song_list)
    selected_song = selected_song.rstrip()
    media = "data/song_media/" + selected_song + ".png"
    #条件を生成

    try:
        api.create_favorite(tw_id)
    except:
        pass
    tweet_url = "https://twitter.com/" + tw_author_screen_name + "/status/" + str(tw_id)
    
    try:
        api.update_with_media(filename=media, status=tweet_buf)
    except:
        traceback.print_exc()
    