import sys
sys.path.append('../')
import TwitterScraper as ts
from SQLConnection import LocalConnection
import TwitterConnection as tc
import format as f


def parse_file_scrape_write(filename, num_tweets, label):
    accounts = get_accounts(filename)
    #scrape 50 at a time, tweepy can only get twitter handles for 50 users at a time
    count = 1 #counts the number of accounts
    start = 0
    end = 50
    while start < len(accounts):
        sliced_accounts = accounts[start:end]
        #Set up tweepy connection
        twit_conn = tc.TwitterConnection()
        users_with_ids = twit_conn.get_user_ids(sliced_accounts)

        #Set up twitter scraper
        rate_delay = 5
        error_delay = 5
        max_tweets = num_tweets
        twit = ts.TwitterSearchImpl(rate_delay, error_delay, max_tweets)

        #set up database connection
        db_name = '../databases/main.db'
        db_conn = LocalConnection(db_name)

        for account in users_with_ids:
            tweets_count = db_conn.get_num_tweets_by(account[0].lower())
            if tweets_count < 500:                        
                 print(str(count) +'/' + str(len(accounts)), account)
                 count += 1
                 print('\t' + account[0], 'has only', tweets_count, 'number of tweets')
#                 write_user(db_conn, account, label)
                 tweets = scrape_tweets(twit, account[0])
                 write_tweets(db_conn, tweets)
                 print('\tAfter:', db_conn.get_num_tweets_by(account[0].lower()))
        start += 50
        end += 50


def get_accounts(filename):
    file = open(filename, 'r')

    accounts = []
    for line in file:
        line = line.rstrip()
        print(line)
        if line != '':
            if line[0] != '#':
                print(line)
                accounts.append(line.rstrip().lower())
    return accounts


def write_user(db_conn, username_and_id, label):
    print('\twriting user', username_and_id[0])
    username = username_and_id[0].lower()
    user_id = username_and_id[1]
    db_conn.write_new_user((username, int(user_id), user_id, label, None))

def write_tweets(db_conn, tweets):
    print('\twriting tweets')
    db_conn.write_tweets(tweets)
    # for tweet in tweets:
    #     tweet_text = f.format_tweet_text(tweet['text'])
    #     db_conn.write_tweet((tweet['tweet_id'], tweet_text, tweet['user_screen_name'].lower(), tweet['created_at']))

def scrape_tweets(twit, username):
    print('\tscraping tweets')
    search_query = 'from:' + username
    twit.search(search_query)
    tweets = twit.get_tweets()
    print("\tNumber of tweets:", len(tweets))
    print("\tTweet counter:", twit.counter)

    twit.clear_tweets()
    return tweets

if __name__  == '__main__':
    filename = input("enter file path: ")
    num_tweets = int(input("number of tweets: "))
    label = input("Political label (conservative/liberal): ")

    filename = '../text_files/dem_reps.txt'
    num_tweets = 20
    label = 'liberal'


    parse_file_scrape_write(filename, num_tweets, label)
