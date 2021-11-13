# -*- coding: utf-8 -*-
from db import db
from models import Serializrable
import datetime

class Equipment(db.Model, Serializrable):
    __tablename__ = 'equipment' 
    #编号
    id = db.Column(db.Integer, db.Sequence('id_seq'), primary_key=True, autoincrement=True)
    equipment_model = db.Column(db.String(80))
    equipment_type = db.Column(db.String(80))
    equipment_name = db.Column(db.String(80))
    equipment_company = db.Column(db.String(120))
    location = db.Column(db.String(120))
    measuring_time = db.Column(db.String(15))
    measuring_period = db.Column(db.String(80))
    measuring_id = db.Column(db.String(80))
    measure_part = db.Column(db.String(80))
    measuring_para = db.Column(db.String(120))
    measuring_res = db.Column(db.String(20))
    status = db.Column(db.String(100))
    action = db.Column(db.String(100))
    def __repr__(self):
         return '(%r, %r)' % (self.id, self.id)