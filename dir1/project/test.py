from tweepy import API
from tweepy import OAuthHandler


import twitter_credentials


if __name__ == "__main__":
    auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
#    auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
    api = API(auth)

    ya = api.favorites('@realDonaldTrump')

    print(ya[0].__dict__.keys())

