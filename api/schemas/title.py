from ma import ma
from marshmallow_enum import EnumField
from models.title import TitleModel, TitleType


class TitleSchema(ma.ModelSchema):
    class Meta:
        model = TitleModel
        strict = True

    title_type = EnumField(TitleType)
