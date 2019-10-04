from flask import Flask, jsonify, send_file, Response
from celery import Celery


app = Flask(__name__)
app.config['CELERY_IMPORTS'] = 'app.tasks'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
app.config['CELERY_TASK_SERIALIZER'] = 'json'
app.config['CELERY_ACCEPT_CONTENT'] = ['application/json']

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

from app import tasks


@app.route('/')
def index():
    return 'Welcome to Celery'

@app.route('/extract')
def extract():
    task = tasks.extract_matches.delay()
    dic = {}
    dic['id'] = task.id
    return jsonify(dic)

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
        path = './app/files/'+ task.result
        with open(path, 'r') as file:
            return Response(file.read(),
                            mimetype="json",
                            headers={"Content-disposition":
                            "attachment; filename="+task.result})
    else:
        return task.info
    return "Some Error"
