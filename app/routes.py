from app import app
from app.tasks import *

@app.route('/')
def index():
    return example(5)