from __future__ import print_function
import json
import datetime
import logging as log
from time import sleep
from concurrent.futures import ThreadPoolExecutor

try:
    from urllib.parse import urlparse, urlencode, urlunparse
except ImportError:
    # Python 2 imports
    from urlparse import urlparse, urlunparse
    from urllib import urlencode

import requests
from abc import ABCMeta
from abc import abstractmethod
from bs4 import BeautifulSoup

__author__ = 'Tom Dickinson'


class TwitterSearch(object):
    __meta__ = ABCMeta

    def __init__(self, rate_delay, error_delay=5):
        """
        :param rate_delay: How long to pause between calls to Twitter
        :param error_delay: How long to pause when an error occurs
        """
        self.rate_delay = rate_delay
        self.error_delay = error_delay

    def search(self, query):
        self.perform_search(query)

    def perform_search(self, query):
        """
        Scrape items from twitter
        :param query:   Query to search Twitter with. Takes form of queries constructed with using Twitters
                        advanced search: https://twitter.com/search-advanced
        """
        url = self.construct_url(query)
        continue_search = True
        min_tweet = None
        response = self.execute_search(url)
        while response is not None and continue_search:
            if 'items_html' in response.keys():
                if response['items_html'] is not None:
                    tweets = self.parse_tweets(response['items_html'])

                    # If we have no tweets, then we can break the loop early
                    if len(tweets) == 0:
                        break

                    # If we haven't set our min tweet yet, set it now
                    if min_tweet is None:
                        min_tweet = tweets[0]

                    continue_search = self.save_tweets(tweets)

                    # Our max tweet is the last tweet in the list
                    max_tweet = tweets[-1]
                    if min_tweet['tweet_id'] is not max_tweet['tweet_id']:
                        if "min_position" in response.keys():
                            max_position = response['min_position']
                        else:
                            max_position = "TWEET-%s-%s" % (max_tweet['tweet_id'], min_tweet['tweet_id'])
                        url = self.construct_url(query, max_position=max_position)
                        # Sleep for our rate_delay
                        print('.')
                        sleep(self.rate_delay)
                        response = self.execute_search(url)

    def execute_search(self, url):
        """
        Executes a search to Twitter for the given URL
        :param url: URL to search twitter with
        :return: A JSON object with data from Twitter
        """
        try:
            # Specify a user agent to prevent Twitter from returning a profile card
            headers = {
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.'
                              '86 Safari/537.36'
            }
            req = requests.get(url, headers=headers)
            # response = urllib2.urlopen(req)
            data = json.loads(req.text)
            return data

        # If we get a ValueError exception due to a request timing out, we sleep for our error delay, then make
        # another attempt
        except Exception as e:
            log.error(e)
            log.error("Sleeping for %i" % self.error_delay)
            sleep(self.error_delay)
            return self.execute_search(url)

    @staticmethod
    def parse_tweets(items_html):
        """
        Parses Tweets from the given HTML
        :param items_html: The HTML block with tweets
        :return: A JSON list of tweets
        """
        soup = BeautifulSoup(items_html, "html.parser")
        tweets = []
        for li in soup.find_all("li", class_='js-stream-item'):

            # If our li doesn't have a tweet-id, we skip it as it's not going to be a tweet.
            if 'data-item-id' not in li.attrs:
                continue

            tweet = {
                'tweet_id': li['data-item-id'],
                'text': None,
                'user_id': None,
                'user_screen_name': None,
                'user_name': None,
                'created_at': None,
                'retweets': 0,
                'favorites': 0
            }

            # Tweet Text
            text_p = li.find("p", class_="tweet-text")
            if text_p is not None:
                tweet['text'] = text_p.get_text()

            # Tweet User ID, User Screen Name, User Name
            user_details_div = li.find("div", class_="tweet")
            if user_details_div is not None:
                tweet['user_id'] = user_details_div['data-user-id']
                tweet['user_screen_name'] = user_details_div['data-screen-name'].lower()
                tweet['user_name'] = user_details_div['data-name']

            # Tweet date
            date_span = li.find("span", class_="_timestamp")
            if date_span is not None:
                t = datetime.datetime.fromtimestamp((float(date_span['data-time-ms']) / 1000))
                fmt = "%Y-%m-%d %H:%M:%S"
                tweet['created_at'] = t.strftime(fmt)

            # Tweet Retweets
            retweet_span = li.select("span.ProfileTweet-action--retweet > span.ProfileTweet-actionCount")
            if retweet_span is not None and len(retweet_span) > 0:
                tweet['retweets'] = int(retweet_span[0]['data-tweet-stat-count'])

            # Tweet Favourites
            favorite_span = li.select("span.ProfileTweet-action--favorite > span.ProfileTweet-actionCount")
            if favorite_span is not None and len(retweet_span) > 0:
                tweet['favorites'] = int(favorite_span[0]['data-tweet-stat-count'])

            tweets.append(tweet)
        return tweets

    @staticmethod
    def construct_url(query, max_position=None):
        """
        For a given query, will construct a URL to search Twitter with
        :param query: The query term used to search twitter
        :param max_position: The max_position value to select the next pagination of tweets
        :return: A string URL
        """

        params = {
            # Type Param
            'f': 'tweets',
            # Query Param
            'q': query
        }

        # If our max_position param is not None, we add it to the parameters
        if max_position is not None:
            params['max_position'] = max_position

        url_tupple = ('https', 'twitter.com', '/i/search/timeline', '', urlencode(params), '')
        return urlunparse(url_tupple)

    @abstractmethod
    def save_tweets(self, tweets):
        """
        An abstract method that's called with a list of tweets.
        When implementing this class, you can do whatever you want with these tweets.
        """


class TwitterSearchImpl(TwitterSearch):

    def __init__(self, rate_delay, error_delay, max_tweets):
        """
        :param rate_delay: How long to pause between calls to Twitter
        :param error_delay: How long to pause when an error occurs
        :param max_tweets: Maximum number of tweets to collect for this example
        """
        super(TwitterSearchImpl, self).__init__(rate_delay, error_delay)
        self.max_tweets = max_tweets
        self.counter = 0
        self.saved_tweets = []
        self.saved_raw_tweets = set()  # just the tweet text

    def save_tweets(self, tweets):
        """
        Just prints out tweets
        :return:
        """
        for tweet in tweets:


            if tweet['created_at'] is not None:
                # log.info("%i [%s] - %s" % (self.counter, tweet['created_at'], tweet['text']))
                if tweet['text'] not in self.saved_raw_tweets:
                    self.saved_tweets.append(tweet)
                    self.saved_raw_tweets.add(tweet['text'])
                    # Lets add a counter so we only collect a max number of tweets
                    self.counter += 1

            # When we've reached our max limit, return False so collection stops
            if self.max_tweets is not None and self.counter >= self.max_tweets:
                return False

        return True

    def get_tweets(self):
        return self.saved_tweets

    def get_raw_tweets(self):
        return list(self.saved_raw_tweets)

    def get_num_tweets(self):
        return len(self.saved_tweets)

    def clear_tweets(self):
        self.saved_tweets = []
        self.saved_raw_tweets = set()
        self.counter = 0


# class TwitterSlicer(TwitterSearch):
#     """
#     Inspired by: https://github.com/simonlindgren/TwitterScraper/blob/master/TwitterSucker.py
#     The concept is to have an implementation that actually splits the query into multiple days.
#     The only additional parameters a user has to input, is a minimum date, and a maximum date.
#     This method also supports parallel scraping.
#     """
#     def __init__(self, rate_delay, error_delay, since, until, n_threads=1):
#         super(TwitterSlicer, self).__init__(rate_delay, error_delay)
#         self.since = since
#         self.until = until
#         self.n_threads = n_threads
#         self.counter = 0
#         self.saved_tweets = []
#
#     def search(self, query):
#         n_days = (self.until - self.since).days
#         tp = ThreadPoolExecutor(max_workers=self.n_threads)
#         for i in range(0, n_days):
#             since_query = self.since + datetime.timedelta(days=i)
#             until_query = self.since + datetime.timedelta(days=(i + 1))
#             day_query = "%s since:%s until:%s" % (query, since_query.strftime("%Y-%m-%d"),
#                                                   until_query.strftime("%Y-%m-%d"))
#             tp.submit(self.perform_search, day_query)
#         tp.shutdown(wait=True)
#
#     def save_tweets(self, tweets):
#         """
#         Just prints out tweets
#         :return: True always
#         """
#         for tweet in tweets:
#             # Lets add a counter so we only collect a max number of tweets
#             self.counter += 1
#             if tweet['created_at'] is not None:
#                 # print(self.counter)
#                 # print('tweet_id', tweet['tweet_id'])
#                 # print('user_id', tweet['user_id'])
#                 # print('created_at', tweet['created_at'])
#                 # print('user_name', tweet['user_name'])
#                 # print(tweet['text'])
#                 # t = datetime.datetime.fromtimestamp((tweet['created_at']/1000))
#                 # fmt = "%Y-%m-%d %H:%M:%S"
#                 # log.info("%i [%s] - %s" % (self.counter, t.strftime(fmt), tweet['text']))
#                 self.saved_tweets.append(tweet)
#         return True
#
#     def get_tweets(self):
#         return self.saved_tweets
#
#     def clear_tweets(self):
#         self.saved_tweets = []

'''
if __name__ == '__main__':
    log.basicConfig(level=log.INFO)

    search_query = "from:realDonaldTrump"
    rate_delay_seconds = 0
    error_delay_seconds = 5


    # Example of using TwitterSearch
    twit = TwitterSearchImpl(rate_delay_seconds, error_delay_seconds, 20)
    twit.search(search_query)

    tweets = twit.get_tweets()

    print(tweets[0].keys())
    for tweet in tweets:
        print(tweet, '\n')
    print('---------------')
    print('---------------')
    print('---------------')


    for i, tweet in enumerate(twit.saved_tweets):
        print(i, '---', tweet)



    # Example of using TwitterSlice
    select_tweets_since = datetime.datetime.strptime("2019-08-01", '%Y-%m-%d')
    select_tweets_until = datetime.datetime.strptime("2019-09-04", '%Y-%m-%d')
    threads = 10

    twitSlice = TwitterSlicer(rate_delay_seconds, error_delay_seconds, select_tweets_since, select_tweets_until,
                              threads)
    twitSlice.search(search_query)

    tweets = twitSlice.get_tweets()
    print(len(tweets))
    for tweet in tweets:
        print(tweet, '\n')

#    print("TwitterSearch collected %i" % twit.counter)
#xprint("TwitterSlicer collected %i" % twitSlice.counter)
'''

if __name__ == '__main__':
    log.basicConfig(level=log.INFO)

    search_query = "from:johnregehr"
    rate_delay_seconds = 0
    error_delay_seconds = 5

    #    Example of using TwitterSearch
    twit = TwitterSearchImpl(rate_delay_seconds, error_delay_seconds, None)
    twit.search(search_query)
    tweets = twit.get_tweets()

    # Example of using TwitterSlice
    '''
    select_tweets_since = datetime.datetime.strptime("2019-08-01", '%Y-%m-%d')
    select_tweets_until = datetime.datetime.strptime("2019-08-02", '%Y-%m-%d')
    threads = 10

    twitSlice = TwitterSlicer(rate_delay_seconds, error_delay_seconds, select_tweets_since, select_tweets_until,
                              threads)
    twitSlice.search(search_query)
    tweets = twitSlice.get_tweets()
    '''
    for tweet in tweets:
        print(tweet)

    print("TwitterSearch collected %i" % twit.counter)
    # print("TwitterSlicer collected %i" % twitSlice.counter)
