from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.task import TaskModel
from datetime import datetime
import dateutil.parser


class TaskList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('path', type=str, required=True, help='This field cannot be left blank')

    def get(self):
        return {'tasks': [source.json() for source in TaskModel.query.all()]}

    def post(self):
        data = Task.parser.parse_args()
        task = TaskModel(data['path'])

        if TaskModel.find_by_path(task.dest_path):
            return {'message': 'Item already exists'}, 400

        task.save_to_db()
        return task.json(), 201


class Task(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('source_path', type=str, help='The path to the source file')
    parser.add_argument('dest_path', type=str, help='The path to the destination file')
    parser.add_argument('time_added', type=dateutil.parser.isoparse, help='Time added in iso format')
    parser.add_argument('time_started', type=dateutil.parser.isoparse, help='Time added in iso format')
    parser.add_argument('time_completed', type=dateutil.parser.isoparse, help='Time added in iso format')
    parser.add_argument('progress', type=int, help='Progress in percent from 0 - 100')
    parser.add_argument('host', type=str, help='Host processing the file')

    def get(self, _id):
        task = TaskModel.find_by_id(_id)

        if task:
            return task.json()
        return {'message': 'Source not found'}, 404

    def delete(self, name):
        pass
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        # return {'message': 'Item deleted'}

    def put(self, _id):
        pass
        data = Task.parser.parse_args()
        task = TaskModel.find_by_id(_id)

        task.source_path = data['source_path']
        task.dest_path = data['dest_path']
        task.time_added = data['time_added']
        task.time_started = data['time_started']
        task.time_completed = data['time_completed']
        task.progress = data['progress']
        task.host = data['host']

        task.save_to_db()
        return task.json()
