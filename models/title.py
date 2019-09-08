from db import db
from enum import Enum
from datetime import datetime, timezone


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
    unkonwn = 'Unknown'


def current_time(context):
    return datetime.now(timezone.utc)


class TitleModel(db.Model):
    __tablename__ = 'titles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    path = db.Column(db.String, unique=True)
    title_type = db.Column(db.Enum(TitleType), default=TitleType.unkonwn)
    file_size = db.Column(db.BigInteger)
    duration = db.Column(db.Integer)
    video_codec = db.Column(db.String)
    video_encoding_settings = db.Column(db.String)
    height = db.Column(db.Integer)
    width = db.Column(db.Integer)
    writing_application = db.Column(db.String)
    time_added = db.Column(db.DateTime, default=current_time)
    time_modified = db.Column(db.DateTime)
    time_updated = db.Column(db.DateTime, default=current_time, onupdate=current_time)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'), nullable=True)
    movie = db.relationship('MovieModel', backref='titles')
    disc_id = db.Column(db.Integer, db.ForeignKey('discs.id', ondelete='CASCADE'), nullable=True)
    disc = db.relationship('DiscModel', backref='titles')

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_path(cls, path):
        return cls.query.filter_by(path=path).first()

    @classmethod
    def search(cls, params):
        q = db.session.query(cls)
        for key, value in params.items():
            # Perform an exact match for columns that require it
            if key == 'id' or key == 'title_type':
                q = q.filter(getattr(cls, key) == value)

            # Perform a like query for everything else
            else:
                q = q.filter(getattr(cls, key).like("%%{}%%".format(value)))
        return q.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
