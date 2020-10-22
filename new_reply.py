import tweepy
import requests
import sys
import random
import MyAPI
import traceback
import re
import pathlib

auth = tweepy.OAuthHandler(MyAPI.consumer_key_send, MyAPI.consumer_secret_send)
auth.set_access_token(MyAPI.access_token_send, MyAPI.access_secret_send)
api = tweepy.API(auth)


# def serch_level(text, LV_start, LV_end):
#     for i in range(int(LV_start * 10), int(LV_end * 10) + 1):
#         if (str(i / 10) in text):
#             return str(i / 10)
#         elif str(i / 10) in text:
#             return str(int(i / 10))
#     for i in range(int(LV_start), int(LV_end) + 1):
#         if ((str(i) + "+" in text) or (str(i) + "＋" in text)) and (i != 14):
#             return (str(i) + "+")
#         elif str(i) in text:
#             return str(i)
#     return "ALL"

def find_level(tweet):
    levels = []
    tweet = tweet.replace('＋', '+')
    for level in re.findall("1[0-3]\+|1[0-4]\.[0-9]|1[0-4]", tweet):
        levels.append(level)
    if len(levels) == 0:
        return ['random']
    else:
        return levels


def choice_song(levels):
    choiced_songs = []
    for i in range(len(levels)):
        path = "test_data/" + levels[i] + "/"
    # print(path)
        songs = []
        for song in pathlib.Path(path).glob("*.png"):
            songs.append({"file_path": song, "file_name": str(
                song)[:-4].replace(path, '')})
        choiced_songs.append(random.choice(songs))
    return choiced_songs

def generating_challenge():
    notes_decision = ("JUSTICE", "ATTACK", "MISS")
    Riquest_JUSTICE = (1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150)
    Riquest_ATTACK_or_MISS = (1, 5, 10, 20, 30)
    
    choiced = random.choice(notes_decision)
    if choiced == notes_decision[0]:
        return [choiced, random.choice(Riquest_JUSTICE)]
    else:
        return [choiced, random.choice(Riquest_ATTACK_or_MISS)]

# def serch_genre(text):
#     genre_list = []
#     ジャンルの指定をつくる

def reply(tw_text, tw_user_name, tw_id, tw_author_screen_name, tw_retweeted):
    level = find_level(tw_text)[:3]
    print(level)
    update_files = []
    send_tweet = "コースモード: "
    for song_info in choice_song(level):
        print(song_info["file_path"])
        update_files.append(str(song_info["file_path"]))
        send_tweet += "「" + song_info["file_name"] + "」"
    send_tweet += "JUSTICE1以下で終了 "
    media_ids = []
    for filename in update_files:
        res = api.media_upload(filename)
        media_ids.append(res.media_id)
    try:
        api.create_favorite(tw_id)
    except:
        pass
    tweet_url = "https://twitter.com/" + tw_author_screen_name + "/status/" + str(tw_id)
    send_tweet += tweet_url
    try:
        api.update_status(status=send_tweet, media_ids=media_ids)
    except:
        traceback.print_exc()
    
