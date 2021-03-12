# encoding:UTF-8 

from db import db
from models import Serializrable
import datetime

class Message(db.Model, Serializrable):
    __tablename__ = 'messages' 
    #消息id
    message_id = db.Column(db.Integer, db.Sequence('id_seq'), primary_key=True, autoincrement=True)
    #消息名
    message_name = db.Column(db.String(20), nullable=False)
   
    #message状态 0:未读 1 已读
    message_satus = db.Column(db.Integer, nullable=False)
    #message type: 0:入库申请 1 出库申请 2 等待入库 3 报损消息 4 工单分配 5 入库申请通过
    message_type = db.Column(db.Integer)
    #创建消息账号
    create_name = db.Column(db.String(80), nullable=False)
    #接收账号
    recipient_name = db.Column(db.String(80), nullable=False)
   
    #消息内容
    message_notes = db.Column(db.String(256))
   
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
        
    def __repr__(self):
         return '(%r, %r)' % (self.message_id)