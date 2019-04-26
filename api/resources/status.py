from db import db
from flask_restful import Resource, request
from models.task import TaskModel
import json


class TaskStatus(Resource):

    def get(self):
        counts = TaskModel.count_by_state()
        return counts