from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from celery import Celery

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def make_celery(app):
    celery = Celery(
        'worker',
        broker='redis://localhost:6379/'
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)


from app import models, routes, tasks
