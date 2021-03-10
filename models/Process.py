# encoding:UTF-8 

from db import db
from models import Serializrable
import datetime

class Process(db.Model, Serializrable):
    __tablename__ = 'processes' 
    #工序id
    process_id = db.Column(db.Integer, db.Sequence('id_seq'), primary_key=True, autoincrement=True)
    #工序名
    process_name = db.Column(db.String(20), nullable=False)
    #前工序id
    pre_process_id = db.Column(db.Integer)
    #后工序id
    pos_process_id = db.Column(db.Integer)
    #工单id
    incident_id = db.Column(db.Integer, nullable=False) 
    #工序状态
    process_status = db.Column(db.Integer, nullable=False)
    #工序状态1（备用）
    process_status1 = db.Column(db.Integer)
    #计划开始时间
    start_time_d = db.Column(db.Date)
    #计划结束时间
    end_time_d = db.Column(db.DateTime)
    #工时
    range_time = db.Column(db.Integer)
    #工序参数
    process_parameters = db.Column(db.String(80))
    #工序备注
    process_notes = db.Column(db.String(80))
    #实验负责人
    experiment_owner = db.Column(db.String(20), nullable=False)
    #工序负责人
    process_owner = db.Column(db.String(20))
    #实验员
    experimenter = db.Column(db.String(20))
    #步骤
    step_number = db.Column(db.Integer, nullable=False)
    #实验单id
    experiment_sheet_id = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

        
    def __repr__(self):
         return '(%r, %r)' % (self.process_name, self.process_status)