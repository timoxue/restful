# encoding:UTF-8 

from db import db
from models import Serializrable
import datetime

class FileTempModel(db.Model, Serializrable):
    __tablename__ = 'filetemp' 
    id = db.Column(db.Integer, db.Sequence('id_seq'), primary_key=True, autoincrement=True)
    f_key = db.Column(db.String(80), nullable=False)
    f_des = db.Column(db.String(80), nullable=False)
    f_id = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    is_delete = db.Column(db.Boolean())

    def __repr__(self):
        return '<File %r>' % self.f_id