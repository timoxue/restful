# encoding:UTF-8 

from db import db
from models import Serializrable
import datetime

class Experiment(db.Model, Serializrable):
    __tablename__ = 'experiments' 
    #工序模板id
    experiment_id = db.Column(db.Integer, db.Sequence('id_seq'), primary_key=True, autoincrement=True)
    #工序模板名称
    experiment_name = db.Column(db.String(20),nullable=False)
    #派工Step
    experi_step = db.Column(db.Integer)
    #派工类型名称
    experi_type = db.Column(db.String(20), nullable=False)
    #派工类型描述
    experi_des = db.Column(db.String(80))
    def __repr__(self):
         return '(%r, %r)' % (self.experiment_id, self.experiment_name)