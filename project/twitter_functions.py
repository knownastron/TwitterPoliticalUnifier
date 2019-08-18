import requests
from bs4 import BeautifulSoup
import json
import re

import format.py

def get_liked_list(tweet_id):
    # get the data of likers
    r = requests.get('https://twitter.com/i/activity/favorited_popup?id='+tweet_id)
    # use the grep in order to get the retweeters
    text = r.text
    likers = re.findall('div class=\\\\"account  js-actionable-user js-profile-popup-actionable \\\\" data-screen-name=\\\\"(.+?)\\\\" data-user-id=\\\\"', text)
    return likers


def getTextOfTweets(username, num_tweets):
    '''
    Gets all the texts of a tweet:
    - uses formatText
    - does not include retweets
    '''
    tweet_texts = []
    for status in Cursor(api.user_timeline, screen_name=username, tweet_mode="extended").items(num_tweets):
        if status.full_text[:2] == 'RT':
            continue
        tweet_texts.append(format.formatTweetText(status.full_text))
    return tweet_texts

def get_followers(username):
    '''
    Get list of follower's usernames
    '''
    follower_list = []
    for follower in Cursor(api.followers, screen_name=username).items():
        follower_list.append(follower.screen_name)
    return follower_list

    
