import sqlite3
import pymysql
from Services import Format


class SQLConnection():
    def __init__(self, conn):
        self.conn = conn;

    def write_twitter_user(self, ScreenName, UserId, UserIdStr, PolLabelPredict, PolLabel=None, Test=0):
        sql = ''' INSERT OR IGNORE INTO TwitterUsers(ScreenName, UserId, UserIdStr, PolLabel, PolLabelPredict, Test)
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
            tweet_text = tweet['text']
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
        sql = "SELECT * FROM TwitterUsers where PolLabel = ?"
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

    '''
    TwitterUsers methods
    '''

    def get_twitter_user(self, screen_name):
        """
        Returns a tuple if exists, None otherwise
        """
        sql = '''SELECT * from TwitterUsers where ScreenName = %s'''
        cur = self.conn.cursor()
        cur.execute(sql, screen_name)
        user = cur.fetchone()
        return user

    def does_twitter_user_exist(self, screen_name):
        """
        Returns a boolean
        """
        sql = '''SELECT EXISTS(SELECT * from TwitterUsers where ScreenName = %s)'''
        cur = self.conn.cursor()
        cur.execute(sql, screen_name)
        does_exist = cur.fetchone()
        return bool(does_exist[0])

    def write_twitter_user(self, screen_name, user_id, user_id_str, pol_label, pol_label_pred=None, test=0):
        """
        Requires 6 items
        """
        sql = ''' INSERT IGNORE INTO TwitterUsers(ScreenName, UserId, UserIdStr, PolLabel, PolLabelPredict, Test)
              VALUES(%s, %s, %s, %s, %s, %s) '''
        cur = self.conn.cursor()
        cur.execute(sql,
                    (Format.Format.format_username(screen_name), user_id, user_id_str, pol_label, pol_label_pred, test))
        self.conn.commit()

    def get_users_by_pol_label(self, pol_label):
        sql = "SELECT * FROM TwitterUsers where PolLabel = %s"
        cur = self.conn.cursor()
        cur.execute(sql, (pol_label,))
        users = cur.fetchall()
        return users

    '''
    Tweets Methods
    '''

    def write_tweet(self, tweet_id, tweet_text, screen_name, date):
        sql = ''' INSERT IGNORE INTO Tweets(TweetId, Text, ScreenName, Date)
              VALUES(%s, %s, %s, %s)'''
        cur = self.conn.cursor()
        cur.execute(sql, (tweet_id, tweet_text, Format.Format.format_username(screen_name), date))
        self.conn.commit()

    def write_tweets(self, tweets):
        sql = ''' INSERT IGNORE INTO Tweets(TweetId, Text, ScreenName, Date)
              VALUES(%s, %s, %s, %s)'''
        cur = self.conn.cursor()
        cur._defer_warnings = True
        for tweet in tweets:
            cur.execute(sql, (
            tweet['tweet_id'], tweet['text'], Format.Format.format_username(tweet['user_screen_name']),
            tweet['created_at']))
        self.conn.commit()

    def write_tweets_temp(self, tweets):
        """
        Used for moving sqlite data to mysql on AWS
        """
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

    '''
    UserProfile Methods
    '''

    def create_user_profile(self, email):
        sql = "INSERT IGNORE INTO UserProfiles SET Email = %s"
        cur = self.conn.cursor()
        cur.execute(sql, (email,))
        self.conn.commit()

    '''
    SearchedTwitterUsers Methods
    '''

    def get_searched_twitter_users(self, email):
        """
        :param email: email of User Profile that searched tweets
        :return: a tuple of (email, screen_name)
        """
        sql = "SELECT * from SearchedTwitterUsers NATURAL JOIN TwitterUsers where Email = %s ORDER BY SearchDate DESC"
        cur = self.conn.cursor()
        cur.execute(sql, (email,))
        twitter_users = cur.fetchall()
        return twitter_users

    def insert_searched_twitter_user(self, email, screen_name, searched_date):
        sql = "INSERT IGNORE INTO SearchedTwitterUsers (Email, ScreenName, SearchDate) VALUES (%s, %s, %s)"
        cur = self.conn.cursor()
        cur.execute(sql, (email, screen_name, searched_date,))
        self.conn.commit()

    def close(self):
        self.conn.close()
