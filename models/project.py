# -*- coding: utf-8 -*-

from db import db
from models import Serializrable
from models.program import Program as Program
import datetime


class Project(db.Model, Serializrable):
    __tablename__ = 'project' 
   
    id = db.Column(db.Integer, db.Sequence('id_seq'),primary_key=True,autoincrement=True)
    pro_name = db.Column(db.String(80), nullable=False,unique=True)
    res_name = db.Column(db.String(80),nullable = False)  
    create_name = db.Column(db.String(80),nullable = False)  
    finish_time = db.Column(db.String(8),nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    company = db.Column(db.String(80),nullable = False) 
    category = db.Column(db.String(80)) 
    postcode = db.Column(db.String(80))
    contact = db.Column(db.String(80),nullable = False)
    tele_phone = db.Column(db.String(80))
    u_email = db.Column(db.String(80))
    address = db.Column(db.String(256))
    #检查单
    #check_id = db.Column(db.Integer)
    program = db.relationship('Program', backref='pro', lazy=True)

    def __repr__(self):
        return '<Project %r>' % self.pro_name