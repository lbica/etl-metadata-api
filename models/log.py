from typing import Dict, Union
from sqlalchemy import func
from datetime import datetime, date

from db import db

LogJSON = Dict[str, Union[int, str, float]]


class LogModel(db.Model):
    __tablename__ = 'logs'

    id = db.Column("LOG_ID", db.Integer, primary_key=True, autoincrement=True)

    # project_name = db.Column("PROJECT_NAME", db.String(255), nullable=False)
    # module_name = db.Column("MODULE_NAME", db.String(255), nullable=False)
    # ins_count = db.Column("INS_COUNT", db.Integer, default=0)

    # id = db.Column("LOG_ID", db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column("PROJECT_NAME", db.String(255), nullable=False)
    module_name = db.Column("MODULE_NAME", db.String(255), nullable=False)
    order_date = db.Column("ORDER_DATE", db.Date, nullable=False)
    dataset_name = db.Column("DATASET_NAME", db.String(255))
    log_message = db.Column("LOG_MESSAGE", db.String(1024))
    log_type = db.Column("LOG_TYPE", db.String(255))
    ins_count = db.Column("INS_COUNT", db.Integer, default=0)
    upd_count = db.Column("UPD_COUNT", db.Integer, default=0)
    del_count = db.Column("DEL_COUNT", db.Integer, default=0)
    merge_count = db.Column("MERGE_COUNT", db.Integer, default=0)
    it_ins_date = db.Column("IT_INS_DATE", db.DateTime, default=func.now())
    it_ins_user = db.Column("IT_INS_USER", db.String(255), nullable=False)

    # store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    # store = db.relationship('StoreModel')

    def __init__(self, project_name: str, module_name: str, order_date: date, ins_count: int, upd_count: int,
                 del_count: int, merge_count: int, it_ins_user: str):
        self.project_name = project_name
        self.module_name = module_name
        self.order_date = order_date
        self.ins_count = ins_count
        self.upd_count = upd_count
        self.del_count = del_count
        self.merge_count = merge_count
        self.it_ins_user = it_ins_user

    #
    # def json(self) -> ItemJSON:
    #     return {'name': self.name, 'price': self.price}

    # @classmethod
    # def find_all(cls) -> List["ItemModel"]:
    #     return cls.query.all()
    #
    # @classmethod
    # def find_by_name(cls, name: str) -> "ItemModel":
    #     return cls.query.all()
    #
    # @classmethod
    # def find_by_id(cls, _id: int) -> "ItemModel":
    #     return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
