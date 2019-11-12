import random
import time
import datetime
import joblib
import celery
from celery import Celery
from Database import SQLConnection
from Database import mysql_aws_credentials
from Services import TwitterScraper
from Services import Format
from Services import TwitterConnection

#temp
import os

config = {
    'CELERY_BROKER_URL': 'redis://localhost:6379/0',
    'CELERY_RESULT_BACKEND': 'redis://localhost:6379/0'
}

#Set up Celery
celery = Celery('Tasks', broker=config['CELERY_BROKER_URL'])
celery.conf.update(config)

#Set up db
aws_conn = SQLConnection.AWSConnection(mysql_aws_credentials.HOST, mysql_aws_credentials.PORT, mysql_aws_credentials.DATABASE_NAME,
                         mysql_aws_credentials.USER, mysql_aws_credentials.PASSWORD)

#Set up TwitterScrapper and TwitterConnection
rate_delay_seconds = 5
error_delay_seconds = 10
twit_scraper = TwitterScraper.TwitterSearchImpl(rate_delay_seconds, error_delay_seconds, None)

twit_conn = TwitterConnection.TwitterConnection()

#set up NLP and vectorizer
nlp_model = open('./NLP_political_classifier.pkl', 'rb')
clf = joblib.load(nlp_model)

vectorizer_object = open('./tfid_vectorizer.pkl', 'rb')
vectorizer = joblib.load(vectorizer_object)



@celery.task(bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(10, 50)

    print('entered long task function')
    for i in range(total):
        print(i)
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}


@celery.task(bind=True)
def predict_user(self, screen_name, app_user_email):
    cur_user = aws_conn.get_twitter_user(screen_name)
    time_of_search = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if cur_user:
        aws_conn.insert_searched_twitter_user(app_user_email, screen_name, time_of_search)
        return {'status': 'already existed' }


    user_id = twit_conn.get_user_ids([screen_name])[0][1]
    print('GOT USER ID', user_id)
    search_query = "from:" + screen_name
    twit_scraper.search(search_query)

    tweets = twit_scraper.get_raw_tweets()
    tweets = ' '.join(tweets)
    print('GOT TWEETS')

    cleaned_text = Format.Format.denoise_tweet(tweets)
    cleaned_text = Format.Format.stem_words_str(cleaned_text)
    print('CLEANED TWEETS')

    vectorized_text = vectorizer.transform([cleaned_text])
    prediction = clf.predict(vectorized_text)[0]
    print('PREDICTED', prediction)

    aws_conn.write_twitter_user(screen_name, int(user_id), user_id, prediction)
    print('WROTE NEW USER')
    aws_conn.insert_searched_twitter_user(app_user_email, screen_name, time_of_search)
    print('WROTE SEARCHED')
    return {'status': 'added new user'}

@celery.task(bind=True)
def get_searched_users(self, app_user_email):
    print('entered get_searched_users')
    searched_users = aws_conn.get_searched_twitter_users(app_user_email)
    return searched_users

@celery.task(bind=True)
def create_new_user(self, email):
    aws_conn.create_user_profile(email)
    return

@celery.task(bind=True)
def predict_tweet(self, screen_name, tweet_id, app_user):
    pass
    #if tweet already in db,
        # update app_user's profile

    #else
        # get screen name of likers
        # scrape tweets of all users
        # run it through NLP
        # update app_user's profile
