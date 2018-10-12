from flask_restful import Resource, reqparse
from models.task import TaskModel


class NextTask(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('host', type=str, required=True, help='This field cannot be left blank')

    def post(self):
        data = NextTask.parser.parse_args()
        task = TaskModel.next_task()

        if not task:
            return {'message': 'No tasks ready for processing.'}, 204

        task.host = data['host']
        task.save_to_db()

        return task.json(), 201
