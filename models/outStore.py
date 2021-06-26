# -*- coding: utf-8 -*-

from db import db
from models import Serializrable
import datetime


class outStore(db.Model, Serializrable):
    __tablename__ = 'outstore' 
   
    id = db.Column(db.Integer, db.Sequence('id_seq'),primary_key=True,autoincrement=True)
    #出库类型
    is_type = db.Column(db.Integer, nullable=False) #1已完成样品
    #出库时间
    out_date = db.Column(db.String(8),nullable = False)
    #大纲编号
    program_code = db.Column(db.String(80))
    #委托单号
    order_number = db.Column(db.String(80))
    #试验件数量
    is_num = db.Column(db.Integer, nullable=False)
    #领取人
    out_name = db.Column(db.String(80))
    create_name = db.Column(db.String(80),nullable = False)
   
    #备注
    remarks =  db.Column(db.String(120))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)


    def __repr__(self):
         return '(%r, %r)' % (self.order_number, self.id)