import sqlite3

class DatabaseConnection():
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)

    def write_conservative(self, info):
        """
        info:
        """
        sql = ''' INSERT INTO Users(ScreenName, UserId, PolLabel)
              VALUES(?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, info)
        self.conn.commit()

    def write_new_user(self, info):
        """
        Requires 4 items for info, use None if it doesn't exist
        """
        sql = ''' INSERT OR IGNORE INTO Users(ScreenName, UserId, UserIdStr, PolLabel, PolLabelPredict)
              VALUES(?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, info)
        self.conn.commit()

    def write_tweet(self, info):
        sql = ''' INSERT OR IGNORE INTO Tweets(TweetId, Text, ScreenName, Date)
              VALUES(?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, info)
        self.conn.commit()


    def query_all_tweets(self, screen_name):
        sql = "SELECT * FROM Tweets WHERE ScreenName=?"
        cur = self.conn.cursor()
        cur.execute(sql, screen_name)
        tweets = cur.fetchall()
        return tweets

    def query_all_tweets_limit(self, screen_name, limit):
        sql = "SELECT * FROM Tweets WHERE ScreenName=? limit ?"
        cur = self.conn.cursor()
        cur.execute(sql, (screen_name, limit))
        tweets = cur.fetchall()
        return tweets


    def close(self):
        self.conn.close()
