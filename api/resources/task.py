from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.task import TaskModel


class TaskList(Resource):
    def get(self):
        return {'sources': [source.json() for source in TaskModel.query.all()]}


class Task(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file_name', type=str, required=True, help='This field cannot be left blank')
    parser.add_argument('folder', type=str, required=True, help='This field cannot be left blank')
    parser.add_argument('full_path', type=str, required=True, help='This field cannot be left blank')

    def get(self, _id):
        task = TaskModel.get_item_by_id(_id)

        if task:
            return task.json()
        return {'message': 'Source not found'}, 404

    def post(self, name):
        pass
        # if next(filter(lambda x: x['name'] == name, items), None) is not None:
        #     return {'message': 'An item with name {} already exists'.format(name)}, 400
        #
        # data = SourceModel.parser.parse_args()
        # item = {'name': name, 'price': data['price']}
        # items.append(item)
        # return item, 201

    def delete(self, name):
        pass
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        # return {'message': 'Item deleted'}

    def put(self, name):
        pass
        # data = SourceModel.parser.parse_args()
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # if item is None:
        #     item = {'name': name, 'price': data['price']}
        #     items.append(item)
        # else:
        #     item.update(data)
        # return item
