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
    #任务书编码
    task_id = db.Column(db.String(80),nullable = False) 
    #任务书id
    task_form_id = db.Column(db.Integer)
    #试验大纲编码
    program_code = db.Column(db.String(80),nullable = False)  
    #试验大纲id
    program_id = db.Column(db.Integer)
    #任务书名称
    task_name_book = db.Column(db.String(80))
    #委托单时间
    order_time = db.Column(db.String(8),nullable=False)
    #备注
    remarks = db.Column(db.String(120))
    #检测项目名称
    test_item = db.Column(db.String(80))
    #试验任务课题组/合同号
    contract_id = db.Column(db.String(80))
    #样品名称
    sample_name = db.Column(db.String(80))
    #项目材料
    sample_material = db.Column(db.String(80))
    sample_num = db.Column(db.String(80))
    #委托书id
    order_id = db.Column(db.Integer)
    #创建项目时间
    create_time =  db.Column(db.DateTime, default=datetime.datetime.now)
    #创建项目账号
    create_name = db.Column(db.String(80))
    def __repr__(self):
        return '<order_number %r>' % self.order_number