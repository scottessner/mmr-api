from flask_restful import Resource
from models.movie import Movie, MovieSchema

movie_list_schema = MovieSchema(many=True)
movie_schema = MovieSchema()


class MovieList(Resource):

    def get(self):
        movies = Movie.query.all()
        movies_json = movie_list_schema.dump(movies).data
        return {'count': len(movies), 'titles': movies_json}