from db import db
from datetime import datetime, timezone
import os
from enum import Enum
from sqlalchemy.ext.hybrid import hybrid_property, Comparator
import json


class TaskState(Enum):
    open = 'open'
    active = 'active'
    error = 'error'
    complete = 'complete'


class TaskModel(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    source_path = db.Column(db.String)
    dest_path = db.Column(db.String)
    time_added = db.Column(db.DateTime, unique=False)
    time_started = db.Column(db.DateTime, unique=False)
    time_completed = db.Column(db.DateTime, unique=False)
    state = db.Column(db.Enum(TaskState))
    progress = db.Column(db.Integer)
    host = db.Column(db.String(40))

    # tasks = db.relationship('TaskModel', lazy='dynamic')

    def __init__(self, path, time_added=None, host=None, progress=None):
        self.source_path = path
        self.dest_path = os.path.splitext(path)[0] + '.mp4'
        self.time_added = time_added if time_added else datetime.now(timezone.utc)
        self.host = host
        self.state = TaskState.open

    def json(self):
        return {'id': self.id,
                'source_path': self.source_path,
                'dest_path': self.dest_path,
                'time_added': "{}Z".format(self.time_added.isoformat()) if self.time_added else None,
                'time_started': "{}Z".format(self.time_started.isoformat()) if self.time_started else None,
                'time_completed': "{}Z".format(self.time_completed.isoformat()) if self.time_completed else None,
                'state': self.state.name,
                'progress': self.progress,
                'host': self.host}

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_path(cls, path):
        return cls.query.filter_by(dest_path=path).first()

    @classmethod
    def find_by_state(cls, states):
        return cls.query.filter(cls.state.in_(states)).all()

    @classmethod
    def next_task(cls):
        return cls.query.filter(cls.state.is_(TaskState.open)).order_by(cls.time_added).first()

    # @hybrid_property
    # def source_path(self):
    #     return os.path.join(self.folder, self.file_name) + self.source_ext
    #
    # @hybrid_property
    # def dest_path(self):
    #     return os.path.join(self.folder, self.file_name) + self.dest_ext

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

