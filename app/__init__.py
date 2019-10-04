from flask import Flask, url_for

app = Flask(__name__)

from app import tasks


@app.route('/')
def index():
    return 'Welcome to Celery'

@app.route('/task/<time>')
def task(time):
    return tasks.example(int(time))

