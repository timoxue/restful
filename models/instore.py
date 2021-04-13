# -*- coding: utf-8 -*-

from db import db
from models import Serializrable
import datetime


class Instore(db.Model, Serializrable):
    __tablename__ = 'instore' 
   
    id = db.Column(db.Integer, db.Sequence('id_seq'),primary_key=True,autoincrement=True)
    #入库类型
    is_type = db.Column(db.Integer, nullable=False) #0,1,2 入库类型
    #入库时间
    in_date = db.Column(db.String(8),nullable = False)
    #大纲编号
    program_code = db.Column(db.String(80),nullable = False)
    #委托单号
    order_number = db.Column(db.String(80),nullable = False)
    #0申请,1成功,2失败
    is_status = db.Column(db.Integer, nullable=False) 
    #试验件数量
    is_num = db.Column(db.Integer, nullable=False)
    #入库数量
    in_store_num = db.Column(db.Integer, nullable=False,default = 0)
    #审核人姓名
    check_name = db.Column(db.String(80))
    #审核时间
    check_time = db.Column(db.String(8)) 
    
    create_name = db.Column(db.String(80),nullable = False)
    #入库接收人
    store_name = db.Column(db.String(80),nullable = False)
    #入库位置
    location = db.Column(db.String(80),nullable = False)
    #检查单
    check_form_id = db.Column(db.Integer)
    #签字检查单
    sign_check_form_id = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)


    def __repr__(self):
         return '(%r, %r)' % (self.order_number, self.id)