from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Tuna'}
    return render_template('example.html', title='Home', user=user)

