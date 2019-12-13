import random
import time
import datetime
import joblib
import celery
from celery import Celery
from Database import SQLConnection
from Config import mysql_aws_credentials
from Services import TwitterScraper
from Services import Format
from Services import TwitterConnection
from multiprocessing import Manager

# temp
import os

config = {
    'CELERY_BROKER_URL': 'redis://localhost:6379/0',
    'CELERY_RESULT_BACKEND': 'redis://localhost:6379/0',
}

# Set up Celery
celery = Celery('Tasks', broker=config['CELERY_BROKER_URL'], backend=config['CELERY_RESULT_BACKEND'])
# celery.conf.update(config)

# set up dictionary of running tasks for each user
multiprocessing_manager = Manager()
label_user_task_lock = multiprocessing_manager.Lock()
running_user_tasks = multiprocessing_manager.dict()  # {'email' : ('screen_name', 'time_of_search)}

# set up dictionary of running task for each tweet
label_tweet_task_lock = multiprocessing_manager.Lock()
running_tweet_tasks = multiprocessing_manager.dict()  # {'email' : (tweet_id, time_of_search)}

# Set up TwitterScrapper and TwitterConnection
rate_delay_seconds = 15
error_delay_seconds = 10
max_tweets = 200
twit_scraper = TwitterScraper.TwitterSearchImpl(rate_delay_seconds, error_delay_seconds, max_tweets)

twit_conn = TwitterConnection.TwitterConnection()

# set up NLP and vectorizer
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
    self.update_state(state='STARTED')
    print('entered long task function')

    for i in range(total):
        print(i)
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        # self.update_state(state='PROGRESS',
        #                   meta={'current': i, 'total': total,
        #                         'status': message})
        time.sleep(1)
    self.update_state(state='SUCCESS')
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}


@celery.task()
def create_new_user(email):
    aws_conn = SQLConnection.AWSConnection()
    aws_conn.create_user_profile(email)
    return


@celery.task()
def get_searched_users(app_user_email):
    aws_conn = SQLConnection.AWSConnection()
    searched_users = []
    if app_user_email in running_user_tasks:
        for task in running_user_tasks[app_user_email]:
            searched_users.append((task[0], None, str(task[1]), None, None, 'Pending...'))
    searched_users.extend(aws_conn.get_searched_twitter_users(app_user_email))
    # print('******SEARCHED USERS****** ' + str(searched_users))
    return searched_users


@celery.task()
def get_searched_tweets(app_user_email):
    aws_conn = SQLConnection.AWSConnection()
    searched_tweets = []
    with label_tweet_task_lock:
        if app_user_email in running_tweet_tasks:
            # (status['screen_name'], status['id'], time_of_search)
            in_progress = running_tweet_tasks[app_user_email]
            for tweet_task in in_progress:
                searched_tweets.append((app_user_email, tweet_task[1], tweet_task[0], tweet_task[2], tweet_task[3], 'In progress...'))
    db_tweets = aws_conn.get_searched_tweets_by_email(app_user_email)
    searched_tweets.extend(db_tweets)
    # print('******SEARCHED TWEETS****** ' + str(searched_tweets))
    return searched_tweets


@celery.task()
def get_tweet_likes(tweet_id):
    aws_conn = SQLConnection.AWSConnection()
    tweet_like_info = aws_conn.get_tweet_like_info(tweet_id)
    return tweet_like_info


@celery.task()
def predict_user(screen_name, app_user_email):
    aws_conn = SQLConnection.AWSConnection()
    time_of_search = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with label_user_task_lock:
        if app_user_email in running_user_tasks:
            for (cur_screen_name, cur_time) in running_user_tasks[app_user_email]:
                if cur_screen_name == screen_name:
                    return {'status': 'already in progress'}
            add_label_user_task_to_queue(app_user_email, screen_name, time_of_search)
        else:
            running_user_tasks[app_user_email] = [(screen_name, time_of_search)]

    try:
        cur_user = aws_conn.get_twitter_user(screen_name)

        if cur_user:
            aws_conn.insert_searched_twitter_user(app_user_email, screen_name, time_of_search)
            remove_label_user_task_from_queue(app_user_email, screen_name, time_of_search)
            return {'status': 'user already scraped'}

        user_obj = twit_conn.get_user_objects([screen_name])[0]

        aws_conn.insert_searched_twitter_user(app_user_email, screen_name, time_of_search)
        print('WROTE SEARCHED')

    finally:
        # removes the current task from the user tasks
        remove_label_user_task_from_queue(app_user_email, screen_name, time_of_search)
    return {'status': 'added new user'}


@celery.task()
def predict_tweet(app_user_email, tweet_id):
    aws_conn = SQLConnection.AWSConnection()
    time_of_search = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # from this point on use status
    status = twit_conn.get_tweet(tweet_id)
    print('GOT STATUS', status)

    # if tweet search already in progress
    with label_tweet_task_lock:
        if app_user_email in running_tweet_tasks:
            for (cur_screen_name, cur_tweet_id, cur_text, cur_time) in running_tweet_tasks[app_user_email]:
                if cur_tweet_id == status['id']:
                    return {'status': 'already in progress'}
            add_tweet_to_running_tasks(app_user_email, status['screen_name'], status['id'], status['text'], time_of_search)
        else:
            running_tweet_tasks[app_user_email] = [(status['screen_name'], status['id'], status['text'], time_of_search)]

    print(running_tweet_tasks)
    try:
        # checks if tweet has already been searched and predicted before
        previous_tweet = aws_conn.get_searched_tweet_by_id(tweet_id) #status or False

        if previous_tweet is not None:
            aws_conn.insert_searched_tweet(app_user_email, previous_tweet[1], previous_tweet[2], previous_tweet[3], time_of_search)
            return {'status': 'tweet already searched'}

        likers = twit_conn.get_liked_list(tweet_id)

        user_objects_likers = twit_conn.get_user_objects(likers)
        print('number of likers ' + str(len(user_objects_likers)))
        for liker in user_objects_likers:
            does_user_exist = aws_conn.get_twitter_user(liker.screen_name.lower())
            if does_user_exist is None:
                get_tweets(liker, aws_conn)
            else:
                continue
        aws_conn.insert_searched_tweet(app_user_email, status['id'], status['screen_name'], status['text'], time_of_search)
        aws_conn.insert_tweet_likes(likers, tweet_id)
    finally:
        remove_tweet_from_running_tasks(app_user_email, status['screen_name'], status['id'], status['text'], time_of_search)

    return {'status': 'new tweet'}


@celery.task()
def predict_user_tweepy(screen_name, app_user_email):
    aws_conn = SQLConnection.AWSConnection()
    time_of_search = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with label_user_task_lock:
        if app_user_email in running_user_tasks:
            for (cur_screen_name, cur_time) in running_user_tasks[app_user_email]:
                if cur_screen_name == screen_name:
                    return {'status': 'already in progress'}
            add_label_user_task_to_queue(app_user_email, screen_name, time_of_search)
        else:
            running_user_tasks[app_user_email] = [(screen_name, time_of_search)]

    try:
        cur_user = aws_conn.get_twitter_user(screen_name)

        if cur_user:
            aws_conn.insert_searched_twitter_user(app_user_email, screen_name, time_of_search)
            return {'status': 'user already scraped'}

        user_obj = twit_conn.get_user_objects([screen_name])[0]

        get_tweets_tweepy(user_obj, aws_conn)

        aws_conn.insert_searched_twitter_user(app_user_email, screen_name, time_of_search)
        print('WROTE SEARCHED')
    finally:
        # removes the current task from the user tasks
        remove_label_user_task_from_queue(app_user_email, screen_name, time_of_search)
    return {'status': 'added new user'}


@celery.task()
def predict_tweet_tweepy(app_user_email, tweet_id):
    aws_conn = SQLConnection.AWSConnection()
    time_of_search = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # from this point on use status
    status = twit_conn.get_tweet(tweet_id)
    print('GOT STATUS', status)

    # if tweet search already in progress
    with label_tweet_task_lock:
        if app_user_email in running_tweet_tasks:
            for (cur_screen_name, cur_tweet_id, cur_text, cur_time) in running_tweet_tasks[app_user_email]:
                if cur_tweet_id == status['id']:
                    return {'status': 'already in progress'}
            add_tweet_to_running_tasks(app_user_email, status['screen_name'], status['id'], status['text'],
                                       time_of_search)
        else:
            running_tweet_tasks[app_user_email] = [
                (status['screen_name'], status['id'], status['text'], time_of_search)]

    try:
        # checks if tweet has already been searched and predicted before
        previous_tweet = aws_conn.get_searched_tweet_by_id(tweet_id)  # status or False

        if previous_tweet is not None:
            aws_conn.insert_searched_tweet(app_user_email, previous_tweet[1], previous_tweet[2], previous_tweet[3],
                                               time_of_search)
            return {'status': 'tweet already searched'}

        likers = twit_conn.get_liked_list(tweet_id)

        user_objects_likers = twit_conn.get_user_objects(likers)
        print('number of likers ' + str(len(user_objects_likers)))
        for liker in user_objects_likers:
            does_user_exist = aws_conn.get_twitter_user(liker.screen_name.lower())
            if does_user_exist is None:
                get_tweets_tweepy(liker, aws_conn)
            else:
                continue
        aws_conn.insert_searched_tweet(app_user_email, status['id'], status['screen_name'], status['text'],
                                           time_of_search)
        aws_conn.insert_tweet_likes(likers, tweet_id)
    finally:
        remove_tweet_from_running_tasks(app_user_email, status['screen_name'], status['id'], status['text'],
                                        time_of_search)

    return {'status': 'new tweet'}


def add_label_user_task_to_queue(app_user_email, screen_name, time_of_search):
    """
    key and value (a list) must already exist for label_user_task[app_user_email]

    :param app_user_email:
    :param screen_name:
    :param time_of_search:
    :return:
    """
    with label_user_task_lock:
        tasks_for_user = running_user_tasks[app_user_email]
        tasks_for_user.append((screen_name, time_of_search))
        running_user_tasks[app_user_email] = tasks_for_user


def remove_label_user_task_from_queue(app_user_email, screen_name, time_of_search):
    """
    Removes the tuple (screen_name, time_of_search) from the in progress list for a specific user
    :param app_user_email: a string
    :param screen_name: a string
    :param time_of_search: a string
    :return:
    """
    with label_user_task_lock:
        in_progress_for_user = running_user_tasks[app_user_email]
        in_progress_for_user.remove((screen_name, time_of_search))
        running_user_tasks[app_user_email] = in_progress_for_user


def add_tweet_to_running_tasks(app_user_email, screen_name, tweet_id, text, time_of_search):
    with label_tweet_task_lock:
        in_progress_for_user = running_tweet_tasks[app_user_email]
        in_progress_for_user.append((screen_name, tweet_id, text, time_of_search))
        running_tweet_tasks[app_user_email] = in_progress_for_user


def remove_tweet_from_running_tasks(app_user_email, screen_name, tweet_id, text, time_of_search):
    with label_tweet_task_lock:
        in_progress_for_user = running_tweet_tasks[app_user_email]
        in_progress_for_user.remove((screen_name, tweet_id, text, time_of_search))
        running_tweet_tasks[app_user_email] = in_progress_for_user


def get_tweets(user_obj, aws_conn):
    search_query = "from:" + user_obj.screen_name
    print('Searching for: ' + user_obj.screen_name)
    twit_scraper.search(search_query)

    tweets = twit_scraper.get_tweets()
    raw_tweets = twit_scraper.get_raw_tweets()
    tweets_joined = ' '.join(raw_tweets)
    print('GOT TWEETS ' + str(len(tweets)))

    prediction = 'N/A'
    if len(tweets) != 0:
        cleaned_text = Format.Format.denoise_tweet(tweets_joined)
        cleaned_text = Format.Format.stem_words_str(cleaned_text)
        print('CLEANED TWEETS')

        vectorized_text = vectorizer.transform([cleaned_text])
        prediction = clf.predict(vectorized_text)[0]
        print('PREDICTED ' + prediction)

    aws_conn.write_twitter_user(user_obj.screen_name, user_obj.id, user_obj.id_str, prediction, user_obj.location)
    print('WROTE NEW USER')

    # aws_conn.write_tweets(tweets)
    # print('WROTE TWEETS')


def get_tweets_tweepy(user_obj, aws_conn):
    print('Searching for: ' + user_obj.screen_name)

    tweets = twit_conn.get_tweets(user_obj.screen_name)
    raw_tweets = [tweet.text for tweet in tweets]
    tweets_joined = ' '.join(raw_tweets)
    print('GOT TWEETS ' + str(len(tweets)))

    prediction = 'N/A'
    if len(tweets) != 0:
        cleaned_text = Format.Format.denoise_tweet(tweets_joined)
        cleaned_text = Format.Format.stem_words_str(cleaned_text)
        print('CLEANED TWEETS')

        vectorized_text = vectorizer.transform([cleaned_text])
        prediction = clf.predict(vectorized_text)[0]
        print('PREDICTED ' + prediction)


    aws_conn.write_twitter_user(user_obj.screen_name, user_obj.id, user_obj.id_str, prediction, user_obj.location)
    print('WROTE NEW USER')

    
    # aws_conn.write_tweets_status(tweets)
    # print('WROTE TWEETS')

