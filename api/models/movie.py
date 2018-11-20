from db import db
from ma import ma
from marshmallow import fields
from marshmallow_enum import EnumField
from enum import Enum


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    titles = db.relationship('Title', backref='movie', lazy=True)
    time_added = db.Column(db.DateTime, unique=False)
    time_updated = db.Column(db.DateTime, unique=False)


class MovieSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    time_added = fields.DateTime()
    time_updated = fields.DateTime()
