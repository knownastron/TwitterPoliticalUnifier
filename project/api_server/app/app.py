from flask import Flask
from flask import request, url_for, jsonify, Response
from flask_api import status
from flask_cors import CORS



import os #remove later

import json
from Services import Format
from Services import TwitterScraper
from Tasks import Tasks
from Services import Authentication
from Services import Responses
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
    task = Tasks.long_task.apply_async()
    task.wait()
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
def predictUser1():
    data = request.get_json()
    verify = Authentication.check_jwt(data, None)

    if not verify:
        return Responses.auth_error()

    username = data['username']

    # get tweets
    rate_delay_seconds = 0
    error_delay_seconds = 5
    twit = TwitterScraper.TwitterSearchImpl(rate_delay_seconds, error_delay_seconds, 100)
    twit.search('from:' + username.lower())

    tweets = twit.get_raw_tweets()
    print(len(tweets))
    tweets = ' '.join(tweets)

    processed_text = Format.Format.denoise_tweet(tweets)


    # load svm model
    nlp_model = open('./NLP_political_classifier.pkl', 'rb')
    clf = joblib.load(nlp_model)

    # load vectorizer
    vectorizer_object = open('./tfid_vectorizer.pkl', 'rb')
    vectorizer = joblib.load(vectorizer_object)

    vectorized_text = vectorizer.transform([processed_text])
    prediction = clf.predict(vectorized_text)
    return {'username': username, 'politicalLabel': prediction[0]}


@app.route('/api/2.0/getsearchedusers', methods=['POST'])
def get_searched_users():
    data = request.get_json()
    # claims = Authentication.check_jwt(data, None)
    # email = claims['email']
    email = data['email']

    task = Tasks.get_searched_users.apply_async([email])
    task.wait()
    result = task.result
    print(result)
    ret = {'searchedUsers': []}

    for i, user in enumerate(result):
        print(user)
        ret['searchedUsers'].append({'id': i, 'screenName': user[0], 'searchDate': user[2], 'polLabel': user[5]})

    return jsonify(ret)

@app.route('/api/2.0/labeluser', methods = ['POST'])
def predictUser2():
    data = request.get_json()
    # task = Tasks.short_task.delay(data['username'])
    # print(data)
    # verify = Authentication.check_jwt(data, None)
    verify = True # remove later
    if not verify:
        return auth_error()

    task = Tasks.predict_user.apply_async([data['username'], data['email']])
    # task.wait()

    resp = {'status_code': 401}
    return resp


@app.route('/api/2.0/createnewuser', methods = ['POST'])
def create_new_user():
    # insert check token
    data = request.get_json()
    email = data['email']

    Tasks.create_new_user.apply_async([email])

    resp = {'status_code': 200}
    return resp


'''
@app.route('/labelTweet', methods=['POST'])
def labelTweet():
    # recover user id, tweet id, etc.
    # get calling user from their session
    global jobListModel
    jobListModel.labelTweet(current_user, twitter_user_id, tweet_id)
    return 200 OK;
'''

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.errorhandler(401)
def auth_error(error=None):
    message = {
        'status': 401,
        'message': 'Authentication Error'
    }
    resp = jsonify(message)
    resp.status_code = 401

    return resp

if __name__ == '__main__':
   app.run(debug="True", threaded=True)
