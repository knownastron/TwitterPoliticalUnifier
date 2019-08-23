import requests                 
from bs4 import BeautifulSoup
import json
import re
import datetime
from tweepy import TweepError
from tweepy import API
from tweepy import OAuthHandler
from tweepy import Cursor


import format
import twitter_credentials



class TwitterConnection:
    def __init__(self):
        self.auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        self.auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)                  
        self.api = API(self.auth)

    def get_text_of_tweet(self, username, num_tweets):
        '''
        Gets all the texts of a tweet:
        - uses formatText
        - does not include retweets
        '''
        tweet_texts = []
        for status in Cursor(self.api.user_timeline, screen_name=username, tweet_mode="extended").items(num_tweets):
            if status.full_text[:2] == 'RT':
                continue
            tweet_texts.append(format.formatTweetText(status.full_text))
        return tweet_texts

    def get_followers(self, username):
        '''
        Get list of follower's usernames
        '''
        follower_list = []
        items = Cursor(self.api.followers, screen_name=username).items(20)
                        
        for follower in items:
            follower_list.append(format.format_username(follower.screen_name))
            
        return follower_list

    def get_liked_list(self, tweet_id):
        '''
        Returns the list of screen_names of users who liked the param tweet_id
        '''
        # get the data of likers
        r = requests.get('https://twitter.com/i/activity/favorited_popup?id='+tweet_id)
        # use the grep in order to get the retweeters
        text = r.text
        likers = re.findall('div class=\\\\"account  js-actionable-user js-profile-popup-actionable \\\\" data-screen-name=\\\\"(.+?)\\\\" data-user-id=\\\\"', text)
        likers = [format.format_username(x) for x in likers]
        return likers

    def get_usernames_of_liked_tweets_by(self, username):
        '''
        returns the screen_names of the tweets liked by param username
        '''
        favs_result_set = self.api.favorites(username)
        usernames = []
        for fav in favs_result_set:
            usernames.append(format.format_username(fav.author.screen_name))
        return usernames

    def get_all_rate_limit_status(self):
        return self.api.rate_limit_status()

    def print_all_rate_limit_status(self):
        limit_info = self.api.rate_limit_status()['resources']

        for key in limit_info:
            print(type(limit_info[key]))

    def print_used_rate_limit_status(self):
        '''
    
        '''
        resources = self.api.rate_limit_status()['resources']
        resource_type = resources.keys()
        for key in resources:
            resource_group = resources[key]
            for key1 in resource_group:
                limit_info = resource_group[key1]
                if limit_info['remaining'] < limit_info['limit']:
                    print(key1, limit_info['limit'], limit_info['remaining'], self.convert_epoch_seconds(limit_info['reset']))

    def convert_epoch_seconds(self, seconds):
        value = datetime.datetime.fromtimestamp(seconds)
        return value.strftime('%Y-%m-%d %H:%M:%S')



'''
twit_conn = TwitterConnection()
twit_conn.print_used_rate_limit_status()

liked_list = twit_conn.get_liked_list("1151868495824642049")
print(liked_list)

liked_users = twit_conn.get_usernames_of_favorited_tweets_by('@AOC')
print(liked_users)
'''


