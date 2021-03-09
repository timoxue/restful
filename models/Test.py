from db import db
from models import Serializrable

class People(db.Model, Serializrable):   
    id = db.Column(db.Integer, db.Sequence('id_seq'), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False) 
    real_title = db.Column(db.String(120),  nullable=False)
    addresses = db.relationship('Address', backref='person', lazy='dynamic')

    def __repr__(self):
        return '<People %r.%r>' % (self.username, self.real_title)

class Address(db.Model, Serializrable):   
    id = db.Column(db.Integer, db.Sequence('id_seq'), primary_key=True, autoincrement=True)
    username = db.Column(db.String(80),  db.ForeignKey('people.username')) 
    address = db.Column(db.String(120),  nullable=False)

    def __repr__(self):
        return '<Address %r.%r>' % (self.username, self.address)

