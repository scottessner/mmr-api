from flask_restful import Resource
from models.task import TaskModel


class TaskStatus(Resource):

    def get(self):
        counts = TaskModel.count_by_state()
        return counts