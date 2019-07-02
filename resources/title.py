from db import db
from flask_restful import Resource, request
from models.title import TitleModel
from schemas.title import TitleSchema
from models.task import TaskType
from schemas.task import TaskSchema


title_list_schema = TitleSchema(many=True, session=db.session)
title_schema = TitleSchema(session=db.session)
task_schema = TaskSchema(session=db.session)


class TitleList(Resource):

    def get(self):
        titles = TitleModel.query.all()
        titles_json = title_list_schema.dump(titles).data
        return titles_json

    def post(self):
        req_data = request.get_json()
        try:
            title = title_schema.load(req_data).data
            if TitleModel.find_by_path(req_data['path']):
                return {'message': 'Item already exists'}, 400

            title.save_to_db()
            # If the title is new, create a task to scan for media info
            task = task_schema.load({'type': TaskType.title_info}).data
            task.title = title
            task.save_to_db()
            return title_schema.dump(title).data, 201

        except AssertionError as e:
            return {'message': str(e)}, 400


class Title(Resource):

    def get(self, _id):
        title = TitleModel.find_by_id(_id)

        if title:
            return title_schema.dump(title).data

    def put(self, _id):
        req_data = request.get_json()
        title = title_schema.load(req_data, instance=TitleModel.find_by_id(_id)).data
        title.save_to_db()

        # Hooks for starting other tasks based on updated information
        if 'path' in req_data.keys():
            # If the path of the title has changed, scan the new file for media info
            task = task_schema.load({'type': TaskType.title_info}).data
            task.title = title
            task.save_to_db()

        return title_schema.dump(title).data, 201


class TitleQuery(Resource):

    def get(self):
        query = request.args
        titles = TitleModel.search(query)
        return title_list_schema.dump(titles).data
