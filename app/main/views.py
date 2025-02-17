from flask import render_template, jsonify
from . import main

@main.route('/')
def home():
    return render_template('index.htm')