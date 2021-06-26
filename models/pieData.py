# encoding:UTF-8 

from db import db
from models import Serializrable
import datetime

class PieData(db.Model, Serializrable):
    __tablename__ = 'piedata' 
    #试验件id
    id = db.Column(db.Integer, db.Sequence('id_seq'), primary_key=True, autoincrement=True)
    data_type = db.Column(db.String(80), unique=True)
    count = db.Column(db.Integer)
   
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    def __repr__(self):
         return '(%r, %r)' % (self.data_type, self.count)