from db import db
from datetime import datetime, timezone
from enum import Enum


class TaskState(Enum):
    open = 'open'
    active = 'active'
    error = 'error'
    complete = 'complete'


class TaskType(Enum):
    preview = 'preview'
    compress = 'compress'
    rename = 'rename'
    remux = 'remux'


class TaskModel(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    time_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    time_updated = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    time_started = db.Column(db.DateTime, unique=False)
    time_completed = db.Column(db.DateTime, unique=False)
    state = db.Column(db.Enum(TaskState), default=TaskState.open)
    type = db.Column(db.Enum(TaskType), nullable=False)
    progress = db.Column(db.Integer)
    host = db.Column(db.String(40))
    title_id = db.Column(db.Integer, db.ForeignKey('titles.id', ondelete='CASCADE'), nullable=False)
    title = db.relationship('TitleModel', backref='tasks')

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
    def next_task(cls, host):
        next_task = cls.query.filter(cls.state.is_(TaskState.open)).order_by(cls.time_added).first()
        if next_task:
            next_task.host = host
            next_task.state = TaskState.active
            next_task.save_to_db()
        return next_task

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

