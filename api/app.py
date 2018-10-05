from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.task import Task, TaskList
# from resources.task import Task, Task

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mmr-api.db'
app.secret_key = 'ernie'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Task, '/task/<int:id>')
api.add_resource(TaskList, '/tasks')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run()

