from flask_restful import Resource, request
from models.movie import MovieModel
from schemas.movie import MovieSchema
from db import db

movie_list_schema = MovieSchema(many=True, session=db.session)
movie_schema = MovieSchema(session=db.session)


class MovieList(Resource):

    def get(self):
        movies = MovieModel.query.all()
        movies_json = movie_list_schema.dump(movies).data
        return movies_json

    def post(self):
        data = request.get_json()
        try:
            movie = movie_schema.load(data).data
        except AssertionError as e:
            return {'message': str(e)}, 400

        movie.save_to_db()

        return movie_schema.dump(movie).data, 201


class Movie(Resource):

    def get(self, _id):
        movie = MovieModel.find_by_id(_id)

        if movie:
            return movie_schema.dump(movie).data
