# encoding:UTF-8 

from db import db
from models import Serializrable
import datetime

class Component(db.Model, Serializrable):
    __tablename__ = 'components' 
    #试验件id
    component_id = db.Column(db.Integer, db.Sequence('id_seq'), primary_key=True, autoincrement=True)
    #试验件名称
    component_name = db.Column(db.String(20), unique=True, nullable=False)
    #试验件编码
    component_unique_id = db.Column(db.String(20), unique=True, nullable=False)
    #工单id
    incident_id = db.Column(db.Integer, nullable=False) 
    #工序id
    process_id = db.Column(db.Integer, nullable=False)
    #试验件状态
    component_status = db.Column(db.Integer, nullable=False)
    #试验件状态1
    component_status1 = db.Column(db.Integer, nullable=False)
    #实验负责人
    experiment_owner = db.Column(db.Integer, nullable=False)
    #工序负责人
    process_owner = db.Column(db.Integer, nullable=False)
    #实验员
    experimenter = db.Column(db.Integer, nullable=False)
    #步骤
    step_number = db.Column(db.Integer, nullable=False)
    #实验单id
    experiment_sheet_id = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    def __repr__(self):
         return '(%r, %r)' % (self.component_name, self.component_unique_id)