# encoding:UTF-8 

from db import db
from models import Serializrable
import datetime

class AlterData(db.Model, Serializrable):
    __tablename__ = 'alterData' 
    #试验件id
    id = db.Column(db.Integer, db.Sequence('id_seq'), primary_key=True, autoincrement=True)
    des = db.Column(db.String(250), unique=True)
   
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    def __repr__(self):
         return '(%r, %r)' % (self.id, self.des)