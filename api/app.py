from flask import Flask
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Column
from sqlalchemy import INTEGER, TEXT, Float, DateTime, TIMESTAMP
from os import path
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/flask/app/web/db/mmr-api.db'
db = SQLAlchemy(app)


class Job(db.Model):
    id = Column(INTEGER, primary_key=True)
    state = Column(TEXT, unique=False)
    file_name = Column(TEXT, unique=False)
    folder = Column(TEXT, unique=False)
    full_path = Column(TEXT, unique=True)
    host = Column(TEXT, unique=False)
    time_added = Column(DateTime, unique=False)
    time_started = Column(TIMESTAMP, unique=False)
    time_completed = Column(TIMESTAMP, unique=False)
    initial_file_size = Column(INTEGER, unique=False)
    final_file_size = Column(INTEGER, unique=False)
    progress = Column(INTEGER, unique=False)

    @property
    def path(self):
        return path.join(self.folder, self.file_name)


def pre_job_post(data=None, **kw):
    data['time_added'] = str(datetime.datetime.now())
    data['state'] = 'waiting'


api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(Job,
                       methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'],
                       preprocessors={
                           'POST': [pre_job_post]
                       })


@app.route('/')
def hello_world():
    return 'Hello World!'


db.create_all()
app.debug = True

if __name__ == '__main__':
    app.run()

