from flask import Flask
from flask import render_template
from flask import request

import os #remove later
import joblib
import json
from Services import Format

app = Flask(__name__)


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

@app.route('api/1.0/labeluser', methods = ['POST'])
def predictUser():
    data = request.get_json()
    username = data['username']



if __name__ == '__main__':
   app.run(debug="True")
