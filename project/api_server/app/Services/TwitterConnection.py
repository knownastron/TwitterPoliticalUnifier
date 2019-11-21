import requests
import re
import time
import datetime
from tweepy import API
from tweepy import OAuthHandler
from tweepy import Cursor
from tweepy import RateLimitError
from Services import Format
from Services import twitter_credentials


def limit_handled(cursor):
    """
    Handles Twitter API's RateLimitError and StopIteration for Cursor
    :param cursor: Tweepy Cursor object
    :return: None
    """
    while True:
        try:
            yield cursor.next()
        except RateLimitError:
            d1 = datetime.datetime.now() + datetime.timedelta(minutes=15)
            print(d1)
            time.sleep(15 * 60)
        except StopIteration:
            break


def convert_epoch_seconds(seconds):
    """
    Converts Twitter's epoch seconds to a human readable time
    :param seconds:
    :return:
    """
    value = datetime.datetime.fromtimestamp(seconds)
    return value.strftime('%Y-%m-%d %H:%M:%S')


class TwitterConnection:
    def __init__(self):
        self.auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        self.auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        self.api = API(self.auth)

    def get_tweet(self, tweet_id):
        """
        Returns the a dict with keys screen_name, id, text, created_at

        :param tweet_id: an int
        :return: a tweepy Status object
        """
        status = self.api.get_status(tweet_id)
        status_dict = {'screen_name': status.author.screen_name.lower(),
                       'id': status.id,
                       'text': status.text,
                       'created_at': status.created_at}
        return status_dict

    def get_text_of_tweet(self, username, num_tweets, print_progress=False):
        """
        Gets all the texts of a tweet:
        - uses formatText
        - does not include retweets
        """
        tweet_texts = []
        count = 1
        for status in limit_handled(Cursor(self.api.user_timeline,
                                           screen_name=username,
                                           tweet_mode="extended").items(num_tweets)):
            if print_progress:
                print('get_text_of_tweet', count)
                count += 1
            if status.full_text[:2] == 'RT':  # skips retweets
                continue
            tweet_texts.append(status.full_text)

        return tweet_texts

    def get_following(self, username, num_followers, print_progress=False):
        """
        Get list of usernames of users followed by param username
        :param username: username in the form of '@name'
        :param num_followers: umber of followers to return
        :param print_progress: True/False for printing progress
        :return: a list of usernames formatted to include '@'
        """
        friend_list = []
        count = 0
        for user in limit_handled(Cursor(self.api.friends, screen_name=username).items(num_followers)):
            cur_following = Format.format_username(user.screen_name)
            friend_list.append(cur_following)
            if print_progress:
                print('get_follower', count, cur_following)
                count += 1
        return friend_list

    def get_followers(self, username, num_followers, print_progress=False):
        """
        Get list of usernames of users that are following param username
        :param username: username in the form of '@name'
        :param num_followers: number of followers to return
        :param print_progress: True/False for print progress
        :return: a list of usernames formatted to include '@'
        """
        follower_list = []
        count = 1
        for follower in limit_handled(Cursor(self.api.followers, screen_name=username).items(num_followers)):
            cur_follower = Format.format_username(follower.screen_name)
            follower_list.append(cur_follower)
            if print_progress:
                print('get_follower', count, cur_follower)
                count += 1
        return follower_list

    def get_liked_list(self, tweet_id):
        """
        Returns the list of usernames of users who liked the param tweet_id

        :param tweet_id: a tweet id as defined by twitter
        :return:a list of usernames formatted to include '@'
        """
        # get the data of likers
        r = requests.get('https://twitter.com/i/activity/favorited_popup?id=' + tweet_id)
        # use the grep in order to get the retweeters
        text = r.text
        likers = re.findall(
            'div class=\\\\"account  js-actionable-user js-profile-popup-actionable \\\\" data-screen-name=\\\\"(.+?)\\\\" data-user-id=\\\\"',
            text)
        likers = [liker.lower() for liker in likers]
        return likers

    def get_usernames_of_tweets_liked_by(self, username, fav_count, print_progress=False):
        """
        returns a list of usernames of the tweets liked by param username
        :param username: username of the target user
        :param fav_count: number of favorited tweets to count
        :param print_progress:
        :return:
        """
        usernames = []
        count = 0
        for fav in limit_handled(Cursor(self.api.favorites, screen_name=username).items(fav_count)):
            cur_user = Format.format_username(fav.author.screen_name)
            usernames.append(cur_user)
            if print_progress:
                print('username_of_tweets_liked_by', count, cur_user)
                count += 1
        return usernames

    def get_user_ids(self, usernames):
        """
        :param usernames: a list of screen names
        :return: list of tuples (username, user_id_str)
        """
        user_objects = self.api.lookup_users(screen_names=usernames)
        user_ids = [(user.screen_name.lower(), user.id_str) for user in user_objects]
        return user_ids

    def get_all_rate_limit_status(self):
        return self.api.rate_limit_status()

    def print_used_rate_limit_status(self):
        """
        Prints the rate limits of resources that have been used
        :return:
        """

        resources = self.api.rate_limit_status()['resources']
        resource_type = resources.keys()
        for key in resources:
            resource_group = resources[key]
            for key1 in resource_group:
                limit_info = resource_group[key1]
                if limit_info['remaining'] < limit_info['limit']:
                    print(key1, limit_info['limit'], limit_info['remaining'],
                          convert_epoch_seconds(limit_info['reset']))

    def get_user_objects(self, usernames):
        """
        keys: 'id', 'id_str', 'name', 'screen_name', 'location'

        :param usernames:
        :return:
        """
        user_objects = self.api.lookup_users(screen_names=usernames)
        return user_objects
