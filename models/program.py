from db import db
from models import Serializrable
from models.instore import Instore as Instore

class Program(db.Model, Serializrable):
    __tablename__ = 'program' 
   
    id = db.Column(db.Integer, db.Sequence('id_seq'), primary_key=True,autoincrement=True)
    pro_name = db.Column(db.String(80), nullable=False,unique=True) 
    pro_id = db.Column(db.Integer,db.ForeignKey('project.id'), nullable=False) 
    task_id = db.Column(db.String(80),nullable = False)  
    task_path = db.Column(db.String(80))
    program_code = db.Column(db.String(80),nullable = False)  
    program_code_path = db.Column(db.String(80))
    task_name_book = db.Column(db.String(80))
    order_time = db.Column(db.String(8),nullable=False)
    remarks = db.Column(db.String(120))
    test_item = db.Column(db.String(80))
    contract_id = db.Column(db.String(80)) 
    sample_name = db.Column(db.String(80))
    sample_material = db.Column(db.String(80))
    sample_num = db.Column(db.String(80))

    def __repr__(self):
        return '<task_id %r>' % self.task_id