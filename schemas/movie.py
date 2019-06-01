from ma import ma
from models.movie import MovieModel


class MovieSchema(ma.ModelSchema):
    class Meta:
        model = MovieModel
        strict = True
    titles = ma.List(ma.Nested('TitleSchema'))
