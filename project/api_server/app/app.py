from flask import Flask
from flask import request, url_for, jsonify, Response
from flask_api import status
from flask_cors import CORS
from Services import Format
from Services import TwitterScraper
from Tasks import Tasks
from Services import Authentication
from Services import Responses

# temp
import json
import joblib

app = Flask(__name__)
CORS(app) # set up CORS

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
    email = data['email']
    auth = Authentication.verify_jwt(data, email)

    if not auth:
        return jsonify({'statusCode': 401,
                        'searchedUsers': [],
                        'message': 'Authentication Error'})

    task_user = Tasks.get_searched_users.apply_async([email])
    task_user.wait()
    result = task_user.result
    # print('-------GET USERS-------', result)
    ret = {'statusCode': 200, 'searchedUsers': []}

    for i, user in enumerate(result):
        #pending users have less than 7 items
        if len(user) < 7:
            ret['searchedUsers'].append({'id': i,
                                         'screenName': user[0],
                                         'searchDate': user[2],
                                         'polLabel': user[5],
                                         'location': '',
                                         'inProgress': True})
        else:
            ret['searchedUsers'].append({'id': i,
                                         'screenName': user[0],
                                         'searchDate': user[2],
                                         'polLabel': user[5],
                                         'location': user[7],
                                         'inProgress': False})
    return jsonify(ret)


@app.route('/api/2.0/labeluser', methods=['POST'])
def predictUser2():
    data = request.get_json()
    email = data['email']
    auth = Authentication.verify_jwt(data, email)

    if not auth:
        return jsonify({'statusCode': 401,
                        'message': 'Authentication Error'})

    task = Tasks.predict_user.apply_async([data['username'], data['email']])

    resp = {'status_code': 200, 'task_id': task.id}
    return resp

@app.route('/api/2.0/labeltweet', methods=['POST'])
def predictTweet2():
    data = request.get_json()
    email = data['email']
    auth = Authentication.verify_jwt(data, email)

    if not auth:
        return jsonify({'statusCode': 401,
                        'message': 'Authentication Error'})

    task = Tasks.predict_tweet.apply_async([data['email'], data['tweetId']])
    resp = {'status_code': 200, 'task_id': task.id}
    return resp


@app.route('/api/2.0/getsearchedtweets', methods=['POST'])
def get_searched_tweets():
    data = request.get_json()
    email = data['email']
    auth = Authentication.verify_jwt(data, email)

    if not auth:
        return jsonify({'statusCode': 401,
                        'searchedTweets': [],
                        'message': 'Authentication Error'})

    task_tweet = Tasks.get_searched_tweets.apply_async([data['email']])
    task_tweet.wait()
    result = task_tweet.result
    # print('--------GET TWEETS------', result)
    ret = {'searchedTweets': []}
    for i, tweet in enumerate(result):
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
    email = data['email']
    auth = Authentication.verify_jwt(data, email)

    if not auth:
        return jsonify({'statusCode': 401,
                        'searchedTweets': [],
                        'message': 'Authentication Error'})

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


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'statusCode': 404,
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
    context = ('/etc/letsencrypt/live/knownastron.com/fullchain.pem',
               '/etc/letsencrypt/live/knownastron.com/privkey.pem')

    app.run(threaded=True, host='0.0.0.0', ssl_context=context)
    # app.run(debug="True", threaded=True)
