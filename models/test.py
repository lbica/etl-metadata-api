from typing import List
from db import db


class TestModel(db.Model):
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False)

    # def __init__(self, name: str):
    #     self.name = name
    #
    # def json(self):
    #     return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name: str) -> "TestModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["TestModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
