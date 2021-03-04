# encoding:UTF-8 

from db import db
from models import Serializrable
import datetime

class FileModel(db.Model, Serializrable):
    __tablename__ = 'files' 
    id = db.Column(db.Integer, db.Sequence('id_seq'), primary_key=True)
    f_filename = db.Column(db.String(80), unique=True, nullable=False)
    f_id = db.Column(db.String(32),unique = True,nullable = False)
    f_location = db.Column(db.String(256),unique = True,nullable = False)
    f_owner = db.Column(db.String(32),unique = True,nullable = False)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    is_delete = db.Column(db.Boolean())

    def __repr__(self):
        return '<User %r>' % self.username