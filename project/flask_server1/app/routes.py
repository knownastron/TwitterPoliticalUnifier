from flask import render_template
from flask import request
from app import app

import os #remove later

import json

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Tuna'}
    return render_template('example.html', title='Home', user=user)


@app.route('/api/1.0/labeluser/<username>', methods = ['GET'])
def predictUsername(username):
    return json.dumps({'username':username, 'label':'conservative'})

@app.route('/api/1.0/labeluser1/', methods = ['GET'])
def predictUsername1():
    username = request.args.get('username')
    return json.dumps({'username':username, 'label':'conservative'})

@app.route('/api/1.0/labeltext', methods = ['POST'])
def predictText():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    files = os.listdir(os.curdir)
    # data = request.get_json()
    # nlp_model = open('./NLP_political_classifier.pkl','rb')
    # clf = joblib.load(nlp_model)
    #
    # vectorizer_object = open('./tfid_vectorizer.pkl', 'rb')
    # vectorizer = joblib.load(vectorizer_object)
    #
    # vectorized_text = vectorizer.transform(data['text'])
    # prediction = clf.predict(vectorized_text)
    return dir_path
