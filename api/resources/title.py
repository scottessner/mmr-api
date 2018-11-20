from flask_restful import Resource
from models.title import Title, TitleSchema

title_list_schema = TitleSchema(many=True)
title_schema = TitleSchema()


class TitleList(Resource):

    def get(self):
        titles = Title.query.all()
        titles_json = title_list_schema.dump(titles).data
        return {'count': len(titles), 'titles': titles_json}