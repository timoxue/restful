# encoding:UTF-8 

from db import db
from models import Serializrable
import datetime

class ComponentHis(db.Model, Serializrable):
    __tablename__ = 'components_his' 
    #试验件id
    id = db.Column(db.Integer, db.Sequence('id_seq'), primary_key=True, autoincrement=True)
    original_id = db.Column(db.String(80))
    #试验件名称
    component_name = db.Column(db.String(20))
    #试验件编码
    component_unique_id = db.Column(db.String(80), nullable=False)
    #委托单单号
    order_number = db.Column(db.String(80),  nullable=False)
    #入库id
    instore_id = db.Column(db.Integer)
    #出库id
    outstore_id = db.Column(db.Integer)
    #工单id
    incident_id = db.Column(db.Integer) 
    #工序id
    process_id = db.Column(db.Integer)
    #试验件状态 0:待入库 1: 确认入库   2:出库
    component_status = db.Column(db.Integer,default=0)
    #试验件状态1  0:待分配 1 已分配 2 实验中 3: 实验结束 4 待审核 5 报废 6 成品
    component_status1 = db.Column(db.Integer)
    #实验负责人
    experiment_owner = db.Column(db.String(20))
    #工序负责人
    process_owner = db.Column(db.String(20))
    #实验员
    experimenter = db.Column(db.String(20))
    #步骤
    step_number = db.Column(db.Integer)
    #实验单id
    experiment_sheet_id = db.Column(db.Integer)
        #是否审核通过   1  通过 2 待审核 
    is_check = db.Column(db.Integer,default = 0)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    def __repr__(self):
         return '( %r)' % ( self.component_unique_id)