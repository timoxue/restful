# encoding:UTF-8 
from db import db
from models import Serializrable
import datetime

class RuleModel(db.Model, Serializrable):
    __tablename__ = 'rules' 
   
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32),  nullable=False) 
    name = db.Column(db.String(80),  nullable = False)
    type = db.Column(db.String(32),nullable = False)  
    des_type = db.Column(db.String(80))
    def __repr__(self):
        return '<id %r>' % self.id

