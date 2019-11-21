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

# Set up db
aws_conn = SQLConnection.AWSConnection(mysql_aws_credentials.HOST, mysql_aws_credentials.PORT,
                                       mysql_aws_credentials.DATABASE_NAME,
                                       mysql_aws_credentials.USER, mysql_aws_credentials.PASSWORD)

# Set up TwitterScrapper and TwitterConnection
rate_delay_seconds = 5
error_delay_seconds = 10
twit_scraper = TwitterScraper.TwitterSearchImpl(rate_delay_seconds, error_delay_seconds, None)

twit_conn = TwitterConnection.TwitterConnection()

# set up NLP and vectorizer
nlp_model = open('./NLP_political_classifier.pkl', 'rb')
clf = joblib.load(nlp_model)

vectorizer_object = open('./tfid_vectorizer.pkl', 'rb')
vectorizer = joblib.load(vectorizer_object)

# set up dictionary of running tasks for each user
multiprocessing_manager = Manager()
label_user_task_lock = multiprocessing_manager.Lock()
label_user_tasks = multiprocessing_manager.dict()  # {'email' : ('screen_name', 'time_of_search)}

# set up dictionary of running task for each tweet
label_tweet_task_lock = multiprocessing_manager.Lock()
label_tweet_tasks = multiprocessing_manager.dict()  # {'email' : (tweet_id, time_of_search)}


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


@celery.task(bind=True)
def predict_user(self, screen_name, app_user_email):
    time_of_search = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with label_user_task_lock:
        if app_user_email in label_user_tasks:
            print('email in task list')
            print(label_user_tasks[app_user_email])
            for (cur_screen_name, cur_time) in label_user_tasks[app_user_email]:
                if cur_screen_name == screen_name:
                    return {'status': 'already in progress'}
            print('appending')
            add_label_user_task_to_queue(app_user_email, screen_name, time_of_search)

        else:
            label_user_tasks[app_user_email] = [(screen_name, time_of_search)]

    # label_user_task_lock.release()
    time.sleep(10)
    cur_user = aws_conn.get_twitter_user(screen_name)

    if cur_user:
        aws_conn.insert_searched_twitter_user(app_user_email, screen_name, time_of_search)
        remove_label_user_task_from_queue(app_user_email, screen_name, time_of_search)
        return {'status': 'user already scraped'}

    try:
        user_id = twit_conn.get_user_ids([screen_name])[0][1]
        print('GOT USER ID', user_id)
        search_query = "from:" + screen_name
        twit_scraper.search(search_query)

        tweets = twit_scraper.get_tweets()
        raw_tweets = twit_scraper.get_raw_tweets()
        tweets_joined = ' '.join(raw_tweets)
        print('GOT TWEETS')

        cleaned_text = Format.Format.denoise_tweet(tweets_joined)
        cleaned_text = Format.Format.stem_words_str(cleaned_text)
        print('CLEANED TWEETS')

        vectorized_text = vectorizer.transform([cleaned_text])
        prediction = clf.predict(vectorized_text)[0]
        print('PREDICTED', prediction)

        aws_conn.write_twitter_user(screen_name, int(user_id), user_id, prediction)
        print('WROTE NEW USER')

        aws_conn.write_tweets(tweets)
        print('WROTE TWEETS')

        aws_conn.insert_searched_twitter_user(app_user_email, screen_name, time_of_search)
        print('WROTE SEARCHED')

        # removes the current task from the user tasks
        remove_label_user_task_from_queue(app_user_email, screen_name, time_of_search)
    finally:
        twit_scraper.clear_tweets()

    return {'status': 'added new user'}


@celery.task(bind=True)
def get_searched_users(self, app_user_email):
    print('entered get_searched_users')
    searched_users = []
    global label_user_tasks
    print(label_user_tasks)
    if app_user_email in label_user_tasks:
        for task in label_user_tasks[app_user_email]:
            searched_users.append((task[0], None, str(task[1]), None, None, 'Pending...'))
    searched_users.extend(aws_conn.get_searched_twitter_users(app_user_email))
    print(searched_users)
    return searched_users


@celery.task(bind=True)
def create_new_user(self, email):
    aws_conn.create_user_profile(email)
    return


@celery.task(bind=True)
def predict_tweet(self, app_user_email, tweet_id):
    time_of_search = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # if tweet search already in progress
    with label_tweet_task_lock:
        if app_user_email in label_tweet_tasks:
            print('email in task list')
            print(label_tweet_tasks[app_user_email])
            for (cur_screen_name, cur_tweet_id, cur_time) in label_user_tasks[app_user_email]:
                if cur_tweet_id == tweet_id:
                    return {'status': 'already in progress'}
            print('appending tweet to task list')
            add_label_user_task_to_queue(app_user_email, screen_name, tweet_id, time_of_search)


    # checks if tweet has already been searched and predicted before
    previous_tweet = aws_conn.get_searched_tweet_by_id(tweet_id) #status or False

    if previous_tweet is not None:
        aws_conn.insert_searched_tweet(app_user_email, previous_tweet[1], previous_tweet[2], previous_tweet[3], time_of_search)
        return {'status': 'tweet already searched'}

    # from this point on use status
    status = twit_conn.get_tweet(tweet_id)
    print('GOT STATUS', status)


    #############################
    likers = twit_conn.get_liked_list(tweet_id)
    likers = ['aoc', 'realdonaldtrump', 'itsleelz']
    #############################

    user_objects_likers = twit_conn.get_user_objects(likers)
    print('len users', len(user_objects_likers))
    for liker in user_objects_likers:
        if aws_conn.get_twitter_user(liker.screen_name.lower()) is None:
            try:
                print('SCRAPING', liker.screen_name.lower())
                search_query = "from:" + liker.screen_name.lower()
                twit_scraper.search(search_query)

                tweets = twit_scraper.get_tweets()
                raw_tweets = twit_scraper.get_raw_tweets()
                tweets_joined = ' '.join(raw_tweets)
                print('GOT TWEETS')

                cleaned_text = Format.Format.denoise_tweet(tweets_joined)
                cleaned_text = Format.Format.stem_words_str(cleaned_text)
                print('CLEANED TWEETS')

                vectorized_text = vectorizer.transform([cleaned_text])
                prediction = clf.predict(vectorized_text)[0]
                print('PREDICTED', prediction)

                aws_conn.write_twitter_user(liker.screen_name.lower(), liker.id, liker.id_str, prediction, liker.location)
                print('WROTE NEW USER')

                aws_conn.write_tweets(tweets)
                print('WROTE TWEETS')
            finally:
                twit_scraper.clear_tweets()
        else:
            print('skipped!')
            continue
    aws_conn.insert_searched_tweet(app_user_email, status[0], status[1], status[2], time_of_search)
    aws_conn.insert_tweet_likes(likers, tweet_id)

    return {'status': 'new tweet'}
    '''
    

    

    
    print('WROTE TWEET LIKES')
    aws_conn.insert_searched_tweet(app_user_email, tweet_id, time_of_search)
    print('WROTE SEARCHED')
    '''
    pass

    # update app_user's profile

    # else
    # get screen name of likers
    # scrape tweets of all users
    # run it through NLP
    # update app_user's profile


def add_label_user_task_to_queue(app_user_email, screen_name, time_of_search):
    """
    key and value (a list) must already exist for label_user_task[app_user_email]

    :param app_user_email:
    :param screen_name:
    :param time_of_search:
    :return:
    """
    # with label_tweet_task_lock:
    tasks_for_user = label_user_tasks[app_user_email]
    tasks_for_user.append((screen_name, time_of_search))
    label_user_tasks[app_user_email] = tasks_for_user


def remove_label_user_task_from_queue(app_user_email, screen_name, time_of_search):
    """
    Removes the tuple (screen_name, time_of_search) from the in progress list for a specific user
    :param app_user_email: a string
    :param screen_name: a string
    :param time_of_search: a string
    :return:
    """
    # label_user_task_lock.acquire()
    in_progress_for_user = label_user_tasks[app_user_email]
    in_progress_for_user.remove((screen_name, time_of_search))
    label_user_tasks[app_user_email] = in_progress_for_user
    # label_user_task_lock.release()


def add_label_tweet_task_to_queue(app_user_email, screen_name, tweet_id, time_of_search):
    in_progress_for_user = label_tweet_tasks[app_user_email]
    in_progress_for_user.append((screen_name, tweet_id, time_of_search))
    label_tweet_tasks[app_user_email] = in_progress_for_user


def remove_label_tweet_task_from_queue(app_user_email, screen_name, tweet_id, time_of_search):
    in_progress_for_user = label_tweet_tasks[app_user_email]
    in_progress_for_user.remove((screen_name, tweet_id, time_of_search))
    label_tweet_tasks[app_user_email] = in_progress_for_user
