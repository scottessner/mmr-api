from db import db
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import func, and_


class TaskState(str, Enum):
    open = 'open'
    active = 'active'
    error = 'error'
    complete = 'complete'


class TaskType(str, Enum):
    preview = 'preview'
    compress = 'compress'
    rename = 'rename'
    remux = 'remux'
    title_info = 'title_info'
    scan = 'scan'


def end_time(context):
    parameters = context.current_parameters
    value = None
    if parameters.get('state') == TaskState.complete:
        value = datetime.now(timezone.utc)
    return value


def current_time(context):
    return datetime.now(timezone.utc)


class TaskModel(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    time_added = db.Column(db.DateTime, default=current_time)
    time_updated = db.Column(db.DateTime, default=current_time, onupdate=current_time)
    time_started = db.Column(db.DateTime, unique=False)
    time_completed = db.Column(db.DateTime, unique=False, onupdate=end_time)
    state = db.Column(db.Enum(TaskState), default=TaskState.open)
    type = db.Column(db.Enum(TaskType), nullable=False)
    progress = db.Column(db.Integer)
    host = db.Column(db.String(40))
    title_id = db.Column(db.Integer, db.ForeignKey('titles.id', ondelete='CASCADE'), nullable=True)
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
    def search(cls, params):
        q = db.session.query(cls)
        for key, value in params.items():
            # Perform an exact match query on fields that require it
            if key == 'state' or key == 'id' or key == 'type':
                q = q.filter(getattr(cls, key) == value)

            # Perform a like query on everything else
            else:
                q = q.filter(getattr(cls, key).like("%%{}%%".format(value)))
        return q.all()

    @classmethod
    def count_by_state(cls):
        count_dict = dict()
        for type in TaskType:
            count_dict[type.value] = dict()
            for state in TaskState:
                count_dict[type.value][state.value] = 0
        counts = cls.query.with_entities(cls.state, cls.type, func.count(cls.state).label('count')).group_by(cls.state, cls.type).all()
        for count in counts:
            count_dict[count.type][count.state] = count.count
        return count_dict

    @classmethod
    def next_task(cls, host):

        # Sequence of tasks with higher priority.  Any types not listed are prioritized by earliest added
        task_priority = (TaskType.scan,
                         TaskType.title_info,
                         TaskType.preview)

        for task_type in task_priority:
            next_task = cls.query.filter(and_(cls.state == TaskState.open, cls.type == task_type)).first()
            if next_task is not None:
                break

        if next_task is None:
            next_task = cls.query.filter(cls.state == TaskState.open).order_by(cls.time_added).first()

        if next_task:
            next_task.host = host
            next_task.state = TaskState.active
            next_task.time_started = datetime.now(timezone.utc)
            next_task.save_to_db()
        return next_task

    def save_to_db(self):
        # self.time_updated = datetime.now(timezone.utc)
        db.session.add(self)
        db.session.commit()

