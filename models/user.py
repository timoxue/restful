from db import db
from models import Serializrable
import datetime

class User(db.Model, Serializrable):
    __tablename__ = 'users' 
   
    id = db.Column(db.Integer, db.Sequence('id_seq'), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False) 
    u_id = db.Column(db.String(32),unique = True,nullable = False)  
    u_password = db.Column(db.String(32),nullable = False) 
    u_authority = db.Column(db.String(256),nullable = False)
    u_createtime = db.Column(db.DateTime, default=datetime.datetime.now)
    u_department = db.Column(db.String(32),nullable = False)
    u_name = db.Column(db.String(256),nullable = False)  
    u_tele = db.Column(db.String(256),nullable = False)  
    is_delete = db.Column(db.Boolean(),default=False)
    u_email = db.Column(db.String(120),  nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

