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
    unable_to_choice = ['10.1', '10.2', '10.4', '10.9', '14.2', '14.3', '14.4', '14.5', '14.6', '14.7', '14.8', '14.9']
    levels = []
    tweet = tweet.replace('＋', '+')
    for level in re.findall("1[0-4]\+|1[0-4]\.[0-9]|1[0-4]", tweet):
        if level not in unable_to_choice:
            levels.append(level)
    if len(levels) == 0:
        return ['random']
    return levels


def choice_song(levels):
    unable_to_choice = ['10.1', '10.2', '10.4', '10.9', '14.2', '14.3', '14.4', '14.5', '14.6', '14.7', '14.8', '14.9']
    for i in range(len(levels)):
        if levels[i] == '10':
            level_a = ['10.0', '10.3', '10.5', '10.6']
            levels[i] = random.choice(level_a)
        elif levels[i] == '10+':
            level_b = ['10.7', '10.8']
            levels[i] = random.choice(level_b)
        elif levels[i] == '14':
            level_c = ['14.0', '14.1']
            levels[i] = random.choice(level_c)
        elif levels[i] == '14+':
            levels[i] = random.choice([str(i / 10) for i in range(100, 142) if str(i / 10) not in unable_to_choice])
    choice_is_random = False
    if levels[0] == 'random':
        levels = levels.remove('random')
        levels = [str(i / 10) for i in range(100, 142) if str(i / 10) not in unable_to_choice]
        choice_is_random = True
    choiced_songs = []
    for i in range(len(levels)):
        path = "data/"
        if "+" in levels[i]:
            path += levels[i] + "/"
            r = [7, 8, 9]
            path += levels[i][:-1] + "." + str(random.choice(r)) + "/"
        elif '.' in levels[i]:
            if int(levels[i][-1]) >= 7:
                path += levels[i][:-2] + "+/" + levels[i] + "/"
            else:
                path += levels[i][:-2] + "/" + levels[i] + "/"
        else:
            path += levels[i] + "/"
            r = [0, 1, 2, 3, 4, 5, 6]
            path += levels[i] + "." + str(random.choice(r)) + "/"
        print(path)
        songs = []
        for song in pathlib.Path(path).glob("*.png"):
            songs.append({"file_path": song, "file_name": str(
                song)[:-4].replace(path, ''), "level_path": path})
        choiced_songs.append(random.choice(songs))
    if (not choice_is_random) and (len(choiced_songs) >= 3):
        return choiced_songs
    else:
        all_songs = []
        for path in choiced_songs:
            for song in pathlib.Path(path["level_path"]).glob("*.png"):
                all_songs.append({"file_path": song, "file_name": str(song)[:-4].replace(path["level_path"], ''), "level_path": path['level_path']})
        if len(choiced_songs) <= 3:
            while len(choiced_songs) < 3:
                choiced_songs.append(random.choice(all_songs))
            return choiced_songs
        else:
            song_returns = []
            while len(song_returns) < 3:
                song_returns.append(random.choice(all_songs))
            return song_returns

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
    # send_tweet += "JUSTICE1以下で終了 "
    print(send_tweet)
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
    
# reply(tw_text="#お願いチュウニペンギン\n13+ 13+ 13", tw_author_screen_name="a", tw_id=1, tw_user_name="a", tw_retweeted=0)