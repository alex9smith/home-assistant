# Contains the main structure of the Flask app
from flask import Flask
from functions import *
from variables import *

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World"