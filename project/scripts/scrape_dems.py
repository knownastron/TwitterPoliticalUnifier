import sqlite3
from tweepy import API
from tweepy import OAuthHandler
from tweepy import Cursor
from tweepy import RateLimitError

import time
import twitter_credentials1
import datetime

auth = OAuthHandler(twitter_credentials1.CONSUMER_KEY, twitter_credentials1.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials1.ACCESS_TOKEN, twitter_credentials1.ACCESS_TOKEN_SECRET)
api = API(auth)

class DatabaseConnection():
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        
    def write_liberal(self, info):
        """
        info: 
        """
        sql = ''' INSERT OR IGNORE INTO Test(ScreenName, UserId, UserIdStr, PolLabel)
              VALUES(?,?,?, ?) '''
        cur = self.conn.cursor()
        cur.execute(sql, info)
        self.conn.commit()
    def close(self):
        self.conn.close()

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

def write_followers(username):
    count = 0
    for follower in limit_handled(Cursor(api.followers, screen_name=username).items()):
        if follower.protected == False:
            info = (follower.screen_name.lower(), follower.id, follower.id_str, 'liberal')
            db_connect.write_liberal(info)
            print(count, info[0:2])
            count += 1

if __name__ == '__main__':
    conservative_db = 'liberals.db'
    db_connect = DatabaseConnection(conservative_db)

write_followers('jaredbrunet')
db_connect.close()
