import bcrypt

from db import db
from common.modelmixin import ModelMixin


class UserModel(db.Model, ModelMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    hashed_password = db.Column(db.String(80))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hashed_password = bcrypt.hashpw(
            kwargs['hashed_password'].encode('utf-8'), bcrypt.gensalt())

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
