from flask_restful import Resource, request
from models.disc import DiscModel
from schemas.disc import DiscSchema
from db import db

disc_list_schema = DiscSchema(many=True, session=db.session, exclude=('titles'))
disc_schema = DiscSchema(session=db.session)


class DiscList(Resource):

    def get(self):
        discs = DiscModel.query.all()
        discs_json = disc_list_schema.dump(discs).data
        return discs_json

    def post(self):
        data = request.get_json()
        try:
            disc = disc_schema.load(data).data
        except AssertionError as e:
            return {'message': str(e)}, 400

        disc.save_to_db()

        return disc_schema.dump(disc), 201


class Disc(Resource):

    def get(self, _id):
        disc = DiscModel.find_by_id(_id)

        if disc:
            return disc_schema.dump(disc).data

    def put(self, _id):
        req_data = request.get_json()
        task = disc_schema.load(req_data, instance=DiscModel.find_by_id(_id)).data
        task.save_to_db()
        return disc_schema.dump(task).data, 201


class DiscScan(Resource):

    def post(self):
        req_data = request.get_json()
        return req_data