from flask import Flask
from flask import request, url_for, jsonify, Response, redirect
from flask_api import status
from flask_cors import CORS

import os  # remove later

import json
from Services import Format
from Services import TwitterScraper
from Tasks import Tasks
from Services import Authentication
from Services import Responses
from celery import Celery
import celery

# temp
import time
import random
import joblib
from celery.task.control import inspect

app = Flask(__name__)
# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# set up CORS
CORS(app)

@app.before_request
def before_request():
    if request.url.startswith('http://'):
        return redirect(request.url.replace('http://', 'https://'), code=301)

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
    return str(status.HTTP_202_ACCEPTED)  # jsonify({}), 202, {'Location': url_for('taskstatus', task_id=task.id)}


@app.route('/api/1.0/labeluser/<username>', methods=['GET', 'OPTIONS'])
def predictUsername(username):
    return json.dumps({'username': username, 'label': 'conservative'})


@app.route('/api/1.0/labeltext', methods=['POST'])
def predictText():
    data = request.get_json()
    text = data['text']

    # load svm model
    nlp_model = open('./NLP_political_classifier.pkl', 'rb')
    clf = joblib.load(nlp_model)

    # load vectorizer
    vectorizer_object = open('./tfid_vectorizer.pkl', 'rb')
    vectorizer = joblib.load(vectorizer_object)

    processed_text = Format.denoise_tweet(text)
    vectorized_text = vectorizer.transform([processed_text])
    prediction = clf.predict(vectorized_text)

    return prediction[0]  # data['text']


@app.route('/api/1.0/labeluser', methods=['POST'])
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


@app.route('/api/2.0/test', methods=['POST'])
def test_2():
    result = Tasks.long_task.apply_async()
    print(result.id)
    return result.id


@app.route('/api/2.0/test2', methods=['POST'])
def test_3():
    data = request.get_json()
    task = Tasks.long_task.AsyncResult(data['id'])
    print(data['id'])
    task.ready()
    return '202 ' + str(task.state)


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

        ret['searchedUsers'].append({'id': i,
                                     'screenName': user[0],
                                     'searchDate': user[2],
                                     'polLabel': user[5],
                                     'location': user[7]})
    return jsonify(ret)


@app.route('/api/2.0/labeluser', methods=['POST'])
def predictUser2():
    data = request.get_json()
    # task = Tasks.short_task.delay(data['username'])
    # print(data)
    # verify = Authentication.check_jwt(data, None)
    verify = True  # remove later
    if not verify:
        return auth_error()

    task = Tasks.predict_user.apply_async([data['username'], data['email']])
    # task.wait()

    resp = {'status_code': 401, 'task_id': task.id}
    return resp

@app.route('/api/2.0/labeltweet', methods=['POST'])
def predictTweet2():
    data = request.get_json()
    verify = True
    if not verify:
        return auth_error()
    task = Tasks.predict_tweet.apply_async([data['email'], data['tweetId']])
    task.wait()
    return '202'

@app.route('/api/2.0/getsearchedtweets', methods=['POST'])
def get_searched_tweets():
    data = request.get_json()
    verify = True
    if not verify:
        return auth_error()
    task = Tasks.get_searched_tweets.apply_async([data['email']])
    task.wait()

    result = task.result
    print(result)
    ret = {'searchedTweets': []}
    for i, tweet in enumerate(result):
        print(tweet)
        if len(tweet) == 6: #in progress tweets have an extra variable
            ret['searchedTweets'].append({'id': i,
                                          'tweetId': tweet[1],
                                          'screenName': tweet[2],
                                          'text': tweet[3],
                                          'searchDate': tweet[4],
                                          'inProgress': True})
        else:
            ret['searchedTweets'].append({'id': i,
                                          'tweetId': tweet[1],
                                          'screenName': tweet[2],
                                          'text': tweet[3],
                                          'searchDate': tweet[4],
                                          'inProgress': False})
    return ret


@app.route('/api/2.0/gettweetlikes', methods = ['POST'])
def get_tweet_likes():
    data = request.get_json()
    task = Tasks.get_tweet_likes.apply_async([data['tweetId']])
    task.wait()
    result = task.result
    ret = {'tweetLikes': []}

    for i, item in enumerate(result):
        ret['tweetLikes'].append({'id': i,
                                  'screenName': item[0],
                                  'userId': item[1],
                                  'polLabel': item[2],
                                  'location': item[3]})

    return ret


@app.route('/api/2.0/createnewuser', methods=['POST'])
def create_new_user():
    # insert check token
    data = request.get_json()
    email = data['email']

    Tasks.create_new_user.apply_async([email])

    resp = {'status_code': 200}
    return resp

@app.route('/.well-known/acme-challenge/<challenge>')
def letsencrypt_check(challenge):
    challenge_response = {
        "pwJPVL9mDADBnkhcbIdSrQzAAKQYQsYQGS1dD2r9s98":"pwJPVL9mDADBnkhcbIdSrQzAAKQYQsYQGS1dD2r9s98.bWMnYKlC23BeLuBqTjKZXkB6W7EreTY20o9YmgElgdU",
        "eo-SD8trw42K0hUmaODjEEKAqT3wvmudRo0kEtS_q34":"eo-SD8trw42K0hUmaODjEEKAqT3wvmudRo0kEtS_q34.bWMnYKlC23BeLuBqTjKZXkB6W7EreTY20o9YmgElgdU   "
    }
    return Response(challenge_response[challenge], mimetype='text/plain')

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
    context = ('/etc/letsencrypt/live/knownastron.com/fullchain.pem', '/etc/letsencrypt/live/knownastron.com/privkey.pem')
    
    app.run(threaded=True, host='0.0.0.0', port=6001, ssl_context=context)
    # app.run(threaded=True, host='0.0.0.0', port=6000)
