import sqlite3
import pymysql
import Format

class SQLConnection():
    def __init__(self, conn):
        self.conn = conn;


    def write_new_user(self, ScreenName, UserId, UserIdStr, PolLabel, PolLabelPredict):
        """
        Requires 4 items for info, use None if it doesn't exist
        """
        sql = ''' INSERT OR IGNORE INTO Users(ScreenName, UserId, UserIdStr, PolLabel, PolLabelPredict)
              VALUES(?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, info)
        self.conn.commit()

    def write_tweet(self, TweetId, Text, ScreenName, Date):
        sql = ''' INSERT OR IGNORE INTO Tweets(TweetId, Text, ScreenName, Date)
              VALUES(?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, (TweetId, Text, ScreenName, Date,))
        self.conn.commit()

    def write_tweets(self, tweets):
        sql = ''' INSERT OR IGNORE INTO Tweets(TweetId, Text, ScreenName, Date)
              VALUES(?, ?, ?, ?)'''
        cur = self.conn.cursor()
        for tweet in tweets:
            tweet_text = Format.format_tweet_text(tweet['text'])
            cur.execute(sql, (tweet['tweet_id'], tweet_text, tweet['user_screen_name'].lower(), tweet['created_at']))
        self.conn.commit()


    def get_all_tweets_by(self, screen_name):
        sql = "SELECT * FROM Tweets WHERE ScreenName=?"
        cur = self.conn.cursor()
        cur.execute(sql, (screen_name,))
        tweets = cur.fetchall()
        return tweets

    def get_all_tweets_by_limit(self, screen_name, limit):
        sql = "SELECT * FROM Tweets WHERE ScreenName=? limit ?"
        cur = self.conn.cursor()
        cur.execute(sql, (screen_name, limit))
        tweets = cur.fetchall()
        return tweets

    def get_num_tweets_by(self, screen_name):
        sql = "SELECT COUNT(*) FROM Tweets where ScreenName=?"
        cur = self.conn.cursor()
        cur.execute(sql, [screen_name])
        count = cur.fetchone()
        return count[0]

    def get_users_by_pol_label(self, pol_label):
        sql = "SELECT * FROM Users where PolLabel = ?"
        cur = self.conn.cursor()
        cur.execute(sql, (pol_label,))
        users = cur.fetchall()
        return users

    def close(self):
        self.conn.close()

class LocalConnection(SQLConnection):
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        super(LocalConnection, self).__init__(self.conn)


class AWSConnection():
    def __init__(self, host, port, dbname, user, password):
        self.conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)

    def write_new_user(self, ScreenName, UserId, UserIdStr, PolLabel, PolLabelPredict):
        """
        Requires 4 items for info, use None if it doesn't exist
        """
        sql = ''' INSERT IGNORE INTO Users(ScreenName, UserId, UserIdStr, PolLabel, PolLabelPredict)
              VALUES(%s, %s, %s, %s, %s) '''
        cur = self.conn.cursor()
        cur.execute(sql, (ScreenName, UserId, UserIdStr, PolLabel, PolLabelPredict))
        self.conn.commit()

    def write_tweet(self, TweetId, Text, ScreenName, Date):
        sql = ''' INSERT IGNORE INTO Tweets(TweetId, Text, ScreenName, Date)
              VALUES(%s, %s, %s, %s)'''
        cur = self.conn.cursor()
        cur.execute(sql, (TweetId, Text, ScreenName, Date))
        self.conn.commit()

    def write_tweets(self, tweets):
        sql = ''' INSERT IGNORE INTO Tweets(TweetId, Text, ScreenName, Date)
              VALUES(%s, %s, %s, %s)'''
        cur = self.conn.cursor()
        cur._defer_warnings = True
        for tweet in tweets:
            tweet_text = format_tweet_text(tweet['text'])
            cur.execute(sql, (tweet['tweet_id'], tweet_text, tweet['user_screen_name'].lower(), tweet['created_at']))
        self.conn.commit()

    def write_tweets_temp(self, tweets):
        sql = ''' INSERT IGNORE INTO Tweets(TweetId, Text, ScreenName, Date)
              VALUES(%s, %s, %s, %s)'''
        cur = self.conn.cursor()
        cur._defer_warnings = True
        for tweet in tweets:
            cur.execute(sql, (tweet[0], tweet[1], tweet[2], tweet[3]))
        self.conn.commit()
        

    def get_all_tweets_by(self, screen_name):
        sql = "SELECT * FROM Tweets WHERE ScreenName=%s"
        cur = self.conn.cursor()
        cur.execute(sql, screen_name)

        tweets = cur.fetchall()
        return tweets


    def get_all_tweets_by_limit(self, screen_name, limit):
        sql = "SELECT * FROM Tweets WHERE ScreenName=%s limit %s"
        cur = self.conn.cursor()
        cur.execute(sql, (screen_name, limit))
        tweets = cur.fetchall()
        return tweets

    def get_num_tweets_by(self, screen_name):
        sql = "SELECT COUNT(*) FROM Tweets where ScreenName=%s"
        cur = self.conn.cursor()
        cur.execute(sql, (screen_name,))
        count = cur.fetchone()
        return count[0]

    def get_users_by_pol_label(self, pol_label):
        sql = "SELECT * FROM Users where PolLabel = %s"
        cur = self.conn.cursor()
        cur.execute(sql, (pol_label,))
        users = cur.fetchall()
        return users


    def close(self):
        self.conn.close()
