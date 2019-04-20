from db import db
from flask_restful import Resource, request
from models.task import TaskModel, TaskType
from models.title import TitleModel
from schemas.task import TaskSchema


task_list_schema = TaskSchema(many=True, session=db.session)
task_schema = TaskSchema(session=db.session)


class TaskList(Resource):

    def get(self):
        tasks = TaskModel.query.all()
        tasks_json = task_list_schema.dump(tasks).data
        return tasks_json

    def post(self):
        req_data = request.get_json()
        try:
            task = task_schema.load(req_data).data

            task.save_to_db()
            return task_schema.dump(task).data, 201

        except AssertionError as e:
            return {'message': str(e)}, 400


class Task(Resource):

    def get(self, _id):
        task = TaskModel.find_by_id(_id)

        if task:
            return task_schema.dump(task).data

    def put(self, _id):
        req_data = request.get_json()
        task = task_schema.load(req_data, instance=TaskModel.find_by_id(_id)).data
        task.save_to_db()
        return task_schema.dump(task).data, 201


class NextTask(Resource):

    def post(self):
        req_data = request.get_json()
        task = TaskModel.next_task(req_data['host'])

        if not task:
            return {'message': 'No tasks ready for processing.'}, 204

        return task.schema.dump(task).data, 201


class TasksByTitle(Resource):

    def post(self, title_id):
        title = TitleModel.find_by_id(title_id)
        req_data = request.get_json()
        try:
            task = task_schema.load(req_data).data
            task.title = title

            task.save_to_db()
            return task_schema.dump(task).data, 201

        except AssertionError as e:
            return {'message': str(e)}, 400

    def get(self, title_id):
        title = TitleModel.find_by_id(title_id)
        return task_list_schema.dump(title.tasks).data
