import tweepy
import requests
import sys
import random
import MyAPI
import traceback

auth = tweepy.OAuthHandler(MyAPI.consumer_key_send, MyAPI.consumer_secret_send)
auth.set_access_token(MyAPI.access_token_send, MyAPI.access_secret_send)
api = tweepy.API(auth)


def serch_level(text, LV_start, LV_end):
    for i in range(int(LV_start * 10), int(LV_end * 10) + 1):
        if (str(i / 10) in text):
            return str(i / 10)
        elif str(i / 10) in text:
            return str(int(i / 10))
    for i in range(int(LV_start), int(LV_end) + 1):
        if ((str(i) + "+" in text) or (str(i) + "＋" in text)) and (i != 14):
            return (str(i) + "+")
        elif str(i) in text:
            return str(i)
    return "ALL"

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
    level = serch_level(tw_text, 12.4, 14.1)
    file = open("data/" + "Lv" + level + ".txt")
    song_list = file.readlines()
    file.close()
    selected_song = random.choice(song_list)
    selected_song = selected_song.rstrip()
    media = "data/song_medias/" + selected_song + ".png"
    #条件を生成
    challenge_request = generating_challenge()
    try:
        api.create_favorite(tw_id)
    except:
        pass
    tweet_url = "https://twitter.com/" + tw_author_screen_name + "/status/" + str(tw_id)
    tweet_buf = "僕の選んだ課題曲は" + "「" + selected_song + "」" + "!!\n" + challenge_request[0] + " " + str(challenge_request[1]) + "以下を目指そう!!\n"+ tweet_url
    try:
        api.update_with_media(filename=media, status=tweet_buf)
    except:
        traceback.print_exc()
    
