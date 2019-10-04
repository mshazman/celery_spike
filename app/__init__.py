from flask import Flask
from celery import Celery


app = Flask(__name__)
app.config['CELERY_IMPORTS'] = 'app.tasks'
celery = Celery('task',broker='redis://localhost:6379', backend='redis://')

from app import tasks


@app.route('/')
def index():
    return 'Welcome to Celery'

@app.route('/task/<time>')
def task(time):
    task = tasks.example.delay(int(time))
    return task.id

@app.route('/task/status/<task_id>')
def status(task_id):
    task = celery.AsyncResult(task_id)
    return task.state


@app.route('/task/result/<task_id>')
def result(task_id):
    task = celery.AsyncResult(task_id)
    print(task.state)
    if task.state=='PENDING':
        return "Task is Being Executed"
    elif task.state=='SUCCESS':
        return task.result
    else:
        return task.info
    return "Some Error"
