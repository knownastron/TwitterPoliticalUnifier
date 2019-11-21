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
        sql = ''' INSERT OR IGNORE INTO Tweets(TweetId, Text, ScreenName, Date) VALUES(?, ?, ?, ?)'''
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

    def get_all_users(self):
        sql = "SELECT * FROM Users"
        cur = self.conn.cursor()
        cur.execute(sql)
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

    def write_twitter_user(self, screen_name, user_id, user_id_str, pol_label, location, test=0):
        """
        Requires 6 items
        """
        sql = ''' INSERT IGNORE INTO TwitterUsers(ScreenName, UserId, UserIdStr, PolLabel, Location, Test)
              VALUES(%s, %s, %s, %s, %s, %s) '''
        cur = self.conn.cursor()
        cur.execute(sql,
                    (Format.Format.format_username(screen_name), user_id, user_id_str, pol_label, location, test))
        self.conn.commit()

    def get_users_by_pol_label(self, pol_label):
        sql = "SELECT * FROM TwitterUsers where PolLabel = %s"
        cur = self.conn.cursor()
        cur.execute(sql, (pol_label,))
        users = cur.fetchall()
        return users

    def update_location(self, screen_name, location):
        sql = "Update TwitterUsers SET Location = %s WHERE ScreenName = %s"
        cur = self.conn.cursor()
        cur.execute(sql, (location, screen_name, ))
        self.conn.commit()

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

    '''
    SearchedTweets Methods
    '''

    def get_searched_tweets_by_email(self, email):
        """
        :param email:
        :return:
        """
        sql = "SELECT * from SearchedTweets NATURAL JOIN Tweets where Email = %s ORDER BY SearchDate DESC"
        cur = self.conn.cursor()
        cur.execute(sql, (email,))
        searched_tweets = cur.fetchall()
        return searched_tweets

    def get_searched_tweet_by_id(self, tweet_id):
        sql = "SELECT * from SearchedTweets where TweetId = %s"
        cur = self.conn.cursor()
        cur.execute(sql, (tweet_id,))
        searched_tweets = cur.fetchone()
        return searched_tweets

    def does_searched_tweet_exist(self, tweet_id):
        sql = "SELECT * from SearchedTweets where TweetId = %s"
        cur = self.conn.cursor()
        cur.execute(sql, (tweet_id,))
        searched_tweet = cur.fetchone()
        return False if searched_tweet is None else searched_tweet

    def insert_searched_tweet(self, email, tweet_id, screen_name, tweet_text, search_date):
        """

        :param email:
        :param tweet_id:
        :param screen_name:
        :param tweet_text:
        :param search_date:
        :return:
        """
        sql = '''INSERT IGNORE INTO SearchedTweets (Email, TweetId, ScreenName, Text, SearchDate)
              VALUES (%s, %s, %s, %s, %s)'''
        cur = self.conn.cursor()
        cur.execute(sql, (email, tweet_id, screen_name, tweet_text, search_date,))
        self.conn.commit()

    '''
    TweetLikes Methods
    '''

    def insert_tweet_likes(self, screen_names, tweet_id):
        """
        :param screen_names: a list of screen names
        :param tweet_id:
        :return:
        """
        sql = "INSERT IGNORE INTO TweetLikes (ScreenName, TweetId) VALUES (%s, %s)"
        cur = self.conn.cursor()
        for screen_name in screen_names:
            cur.execute(sql, (screen_name, tweet_id))
        self.conn.commit()


    def get_screen_name_from_tweet_likes(self, tweet_id):
        sql = "SELECT ScreenName FROM TweetLikes where TweetId = %s"
        cur = self.conn.cursor()
        cur.execute(sql, (tweet_id,))
        screen_names = cur.fetchall()
        return screen_names




    def close(self):
        self.conn.close()
