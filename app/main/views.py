from flask import render_template, jsonify
from . import main
from app.data import Data

@main.route('/')
def home():
    d = Data('Memari')
    return render_template('index.htm', data = d)

@main.get('/hour')
def hour():
    '''This one was a api call which return  hours weather cast'''
    d = Data('Memari')
    hours_data = d.get_hours()
    return jsonify(hour = hours_data)
