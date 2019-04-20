from db import db
from sqlalchemy import UniqueConstraint
from datetime import datetime, timezone
import re

slug_regex = re.compile('(?P<name>.*) \((?P<year>\d{4})\)')


class MovieModel(db.Model):
    __tablename__ = 'movies'
    __table_args__ = (
        UniqueConstraint('name', 'release_year'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    release_year = db.Column(db.Integer)
    tmdb_id = db.Column(db.Integer)
    cover_url = db.Column(db.String)
    time_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    time_updated = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_slug(cls, slug):
        result = slug_regex.match(slug)
        name = result.groupdict().get('name', None)
        year = result.groupdict().get('year', None)
        return cls.query.filter_by(name=name, release_year=year).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
