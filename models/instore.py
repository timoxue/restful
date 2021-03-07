# -*- coding: utf-8 -*-

from db import db
from models import Serializrable


class Instore(db.Model, Serializrable):
    __tablename__ = 'instore' 
   
    id = db.Column(db.Integer, db.Sequence('id_seq'),primary_key=True)
    is_type = db.Column(db.Integer, nullable=False) #0,1,2
    in_date = db.Column(db.String(8),nullable = False)
    program_code = db.Column(db.String(80),nullable = False)
    is_status = db.Column(db.Integer, nullable=False) #0,1,2
    is_num = db.Column(db.Integer, nullable=False)
    in_store_num = db.Column(db.Integer, nullable=False,default = 0)
    check_name = db.Column(db.String(80))
    check_time = db.Column(db.String(8)) 
    create_name = db.Column(db.String(80),nullable = False)
    store_name = db.Column(db.String(80),nullable = False)
    location = db.Column(db.String(80),nullable = False)
    check_form_path = db.Column(db.String(120),nullable = False)

    def __repr__(self):
        return '<Instore %r>' % self.id