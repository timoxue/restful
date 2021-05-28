# -*- coding: utf-8 -*-

from db import db
from models import Serializrable
from models.instore import Instore as Instore
import datetime

class ProgramOutStore(db.Model, Serializrable):
    __tablename__ = 'programOutStore' 
   
    id = db.Column(db.Integer, db.Sequence('id_seq'), primary_key=True,autoincrement=True)
    #项目名称
    pro_name = db.Column(db.String(80), nullable=False,unique=True)    
    #委托单号
    order_number = db.Column(db.String(80),nullable = False)    
    #试验大纲编码
    program_code = db.Column(db.String(80),nullable = False)  
    #样品名称
    sample_name = db.Column(db.String(80))
    sample_material = db.Column(db.String(80))
    sample_num = db.Column(db.String(80))
    create_time =  db.Column(db.DateTime, default=datetime.datetime.now)
    #创建项目账号
    create_name = db.Column(db.String(80))
    def __repr__(self):
        return '<order_number %r>' % self.order_number