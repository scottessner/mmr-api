from ma import ma
from models.disc import DiscModel


class DiscSchema(ma.ModelSchema):
    class Meta:
        model = DiscModel
        strict = True
    titles = ma.List(ma.Nested('TitleSchema'))
    link = ma.URLFor('disc', _id='<id>')
