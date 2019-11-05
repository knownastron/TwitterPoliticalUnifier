from flask import Flask
from flask import request, url_for, jsonify
from flask_api import status
from flask_cors import CORS



import os #remove later

import json
from Services import Format
from Services import TwitterScraper
from Services import CeleryTest
from celery import Celery
import celery

#temp
import time
import random
import joblib

app = Flask(__name__)
# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

#set up CORS
CORS(app)

#Set up Celery
# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)

#jobListModel = JobListModel(database credentials, etc.)

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Tuna'}
    return 'duuhello'

@app.route('/longtask', methods=['POST'])
def longtask():
    print('entered longtask route')
    task = CeleryTest.long_task.apply_async()
    return str(status.HTTP_202_ACCEPTED) # jsonify({}), 202, {'Location': url_for('taskstatus', task_id=task.id)}


@app.route('/api/1.0/labeluser/<username>', methods=['GET', 'OPTIONS'])
def predictUsername(username):
    return json.dumps({'username': username, 'label': 'conservative'})

@app.route('/api/1.0/labeltext', methods = ['POST'])
def predictText():
    data = request.get_json()
    text = data['text']

    #load svm model
    nlp_model = open('./NLP_political_classifier.pkl','rb')
    clf = joblib.load(nlp_model)

    #load vectorizer
    vectorizer_object = open('./tfid_vectorizer.pkl', 'rb')
    vectorizer = joblib.load(vectorizer_object)

    processed_text = Format.denoise_tweet(text)
    vectorized_text = vectorizer.transform([processed_text])
    prediction = clf.predict(vectorized_text)

    return prediction[0] #data['text']

@app.route('/api/1.0/labeluser', methods = ['POST'])
def predictUser():
    data = request.get_json()
    username = data['username']

    # get tweets
    rate_delay_seconds = 0
    error_delay_seconds = 5
    twit = TwitterScraper.TwitterSearchImpl(rate_delay_seconds, error_delay_seconds, 100)
    twit.search('from:' + username.lower())

    tweets = twit.get_raw_tweets()
    print(len(tweets))
    tweets = ' '.join(tweets)

    processed_text = Format.denoise_tweet(tweets)


    # load svm model
    nlp_model = open('./NLP_political_classifier.pkl', 'rb')
    clf = joblib.load(nlp_model)

    # load vectorizer
    vectorizer_object = open('./tfid_vectorizer.pkl', 'rb')
    vectorizer = joblib.load(vectorizer_object)

    vectorized_text = vectorizer.transform([processed_text])
    prediction = clf.predict(vectorized_text)
    return prediction[0]

'''
@app.route('/labelTweet', methods=['POST'])
def labelTweet():
    # recover user id, tweet id, etc.
    # get calling user from their session
    global jobListModel
    jobListModel.labelTweet(current_user, twitter_user_id, tweet_id)
    return 200 OK;
'''

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

if __name__ == '__main__':
   app.run(debug="True", threaded=True)
