# -*- coding: utf-8 -*-

from db import db
from models import Serializrable
from models.instore import Instore as Instore
import datetime

class Program(db.Model, Serializrable):
    __tablename__ = 'program' 
   
    id = db.Column(db.Integer, db.Sequence('id_seq'), primary_key=True,autoincrement=True)
    #项目名称
    pro_name = db.Column(db.String(80), nullable=False,unique=True)
    #项目id
    pro_id = db.Column(db.Integer,db.ForeignKey('project.id'), nullable=False)
    #委托单号
    order_number = db.Column(db.String(80),nullable = False)
    #
    task_id = db.Column(db.String(80),nullable = False) 
    task_path = db.Column(db.String(80))
    program_code = db.Column(db.String(80),nullable = False)  
    program_code_path = db.Column(db.String(80))
    task_name_book = db.Column(db.String(80))
    #委托单时间
    order_time = db.Column(db.String(8),nullable=False)
    #备注
    remarks = db.Column(db.String(120))
    test_item = db.Column(db.String(80))
    contract_id = db.Column(db.String(80)) 
    sample_name = db.Column(db.String(80))
    sample_material = db.Column(db.String(80))
    sample_num = db.Column(db.String(80))
    create_time =  db.Column(db.DateTime, default=datetime.datetime.now)
    #创建项目账号
    #create_name = db.Column(db.String(80),nullable = False)
    def __repr__(self):
        return '<order_number %r>' % self.order_number