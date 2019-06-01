from ma import ma
from models.task import TaskModel, TaskState, TaskType
from marshmallow_enum import EnumField


class TaskSchema(ma.ModelSchema):
    class Meta:
        model = TaskModel
        strict = True
    title = ma.Nested('TitleSchema')
    state = EnumField(TaskState)
    type = EnumField(TaskType)
