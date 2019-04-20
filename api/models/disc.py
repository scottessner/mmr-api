from db import db


class DiscModel(db.Model):
    __tablename__ = 'discs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    path = db.Column(db.String)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_path(cls, path):
        return cls.query.filter_by(path=path).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
