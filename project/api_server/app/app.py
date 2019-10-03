from flask import Flask
from flask import render_template
from flask import request

import os #remove later
import joblib
import json
from Services import Format
from Services import TwitterScraper

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Tuna'}
    return render_template('example.html', title='Home', user=user)


@app.route('/api/1.0/labeluser/<username>', methods = ['GET'])
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


if __name__ == '__main__':
   app.run(debug="True", threaded=True)
