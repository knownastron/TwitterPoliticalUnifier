import twitter_functions as tf
import neo4j_functions as n4j
import format

def get_username_and_tweet_id(url):
    split_url = url.split('/')
    index_of_twitter = split_url.index('twitter.com')
    username = format.format_username(split_url[index_of_twitter + 1])
    tweet_id = split_url[index_of_twitter + 3]
    return username, tweet_id
url = 'https://twitter.com/RonPaul/status/1164231385676222464'
username, tweet_id = get_username_and_tweet_id(url)
twit_conn = tf.TwitterConnection()
neo4j_conn = n4j.Neo4JConnection()

liked_list = twit_conn.get_liked_list(tweet_id)

for user in liked_list:
    print(user, username)
    neo4j_conn.create_liked_relationship(user, username)
    




