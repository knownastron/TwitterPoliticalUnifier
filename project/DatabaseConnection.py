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
        print(info)
        sql = ''' INSERT OR IGNORE INTO Users(ScreenName, UserId, UserIdStr, PolLabel, PolLabelPredict)
              VALUES(?,?,?,?, ?) '''
        cur = self.conn.cursor()
        cur.execute(sql, info)
        self.conn.commit()

    def write_tweet(self, info):
        sql = ''' INSERT OR IGNORE INTO Tweets(TweetId, Text, ScreenName, Date)
              VALUES(?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, info)
        self.conn.commit()



    def close(self):
        self.conn.close()
