from db import db
from datetime import datetime
import os
from sqlalchemy.ext.hybrid import hybrid_property
import json


class TaskModel(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    folder = db.Column(db.String, unique=True)
    file_name = db.Column(db.String)
    source_ext = db.Column(db.String)
    dest_ext = db.Column(db.String)
    time_added = db.Column(db.DateTime, unique=False)
    host = db.Column(db.String(40))

    # tasks = db.relationship('TaskModel', lazy='dynamic')

    def __init__(self, path, time_added=datetime.now(), host=None):
        self.folder, file = os.path.split(path)
        self.file_name, self.source_ext = os.path.splitext()
        self.time_added = time_added
        self.host = host

    def json(self):
        return json.dumps(self)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @hybrid_property
    def source_path(self):
        return os.path.join(self.folder, self.file_name, self.source_ext)

    @hybrid_property
    def dest_path(self):
        return os.path.join(self.folder, self.file_name, self.dest_ext)