from app import db, celery


class Task(db.Model):
    id = db.Column(db.String(64), primary_key=True)

    def get_status(self):
        task = celery.AsyncResult(self.id)
        return task.state

    def __repr__(self):
        return f'<Task: {self.id}>'