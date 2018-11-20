from db import db
from ma import ma
from marshmallow import fields
from marshmallow_enum import EnumField
from enum import Enum


class TitleType(Enum):
    main_feature = 'Main Feature'
    behind_the_scenes = 'Behind The Scenes'
    deleted_scenes = 'Deleted Scenes'
    featurettes = 'Featurettes'
    interviews = 'Interviews'
    scenes = 'Scenes'
    shorts = 'Shorts'
    trailers = 'Trailers'
    episode = 'Episode'


class Title(db.Model):
    __tablename__ = 'titles'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String)
    title_type = db.Column(db.Enum(TitleType))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'), nullable=True)
    time_added = db.Column(db.DateTime, unique=False)
    time_updated = db.Column(db.DateTime, unique=False)


class TitleSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    path = fields.String()
    title_type = EnumField(TitleType, required=True)
    time_added = fields.DateTime()
    time_updated = fields.DateTime()
