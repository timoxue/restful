# encoding:UTF-8 

from db import db
from models import Serializrable
import datetime

class Incident(db.Model, Serializrable):
    __tablename__ = 'incidents' 
    #工单ID
    incident_id = db.Column(db.Integer, db.Sequence('id_seq'), primary_key=True, autoincrement=True)
    #创建工单账号
    create_name = db.Column(db.String(80), nullable=False)
    #委托单号
    order_number = db.Column(db.String(80), nullable=False)
    #检测项目
    experi_project = db.Column(db.String(20))
    #检测依据
    experi_rely = db.Column(db.String(20))
    #派工类型
    experi_type = db.Column(db.String(20))
    #派工id
    #experi_type_id = db.Column(db.Integer)
    #工单状态 = 0:创建，1：实验中,2:完成
    incident_status = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    def __repr__(self):
         return '(%r, %r)' % (self.incident_id, self.order_number)