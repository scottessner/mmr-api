from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db

from resources.task import Task, TaskList
from resources.next import NextTask
# from resources.task import Task, Task

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///db/mmr-api.db'
app.secret_key = 'ernie'
api = Api(app, prefix='/mmr-api/v1')


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Task, '/tasks/<int:_id>')
api.add_resource(TaskList, '/tasks')
api.add_resource(NextTask, '/tasks/next')

db.init_app(app)

print("Name is: {}".format(__name__))
#
# if __name__ == '__main__':
#     from db import db
#     db.init_app(app)
#     app.run()
