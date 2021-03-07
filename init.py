from models.db import db, app
from models.user import User as UserModel
from models.project import Project as ProjectModel
from models.program import Program as ProgramModel
from models.instore import Instore as InstoreModel

from models.Test import People as PeopleModel
from models.Test import Address as AddressModel
from models import Combined
from sqlalchemy.orm import with_polymorphic



import sys,os

if __name__ == '__main__':
    command =  sys.argv[1]
    if command == 'build':
        db.create_all()
        print('created successfully')
    elif command == 'update':
        admin = UserModel(username='admin', u_email='admin@example.com', u_id="123", u_name='what', u_password='123', u_tele = "13888888888", u_authority="jingli", u_department="admin", is_delete=False)
        test_admin = PeopleModel(username='admin', real_title="Manager")
        test_addr= AddressModel(username='admin', address='123')
        test_addr1= AddressModel(username='admin', address='456')
        #guest = UserModel(username='guest', email='guest@example.com')
        db.session.add(admin)
        db.session.add(test_admin)
        db.session.add(test_addr)
        db.session.add(test_addr1)
        db.session.commit()
    elif command == 'clean':
        #db.metadata.clear()
        db.drop_all()
    elif command == 'query': 
        #user = UserModel.query.filter_by(username='admin').first()
        #print(user.email)
        # Option 1
        joined_table = db.session.query(PeopleModel, AddressModel).filter(PeopleModel.username==AddressModel.username) \
                        .all()
        print(type(joined_table[0]))
        #test1
        anmo_rest = Combined(PeopleModel, AddressModel).exclude(['id'], ['id']).to_dict(joined_table)
        print(anmo_rest)
        #test2
        #user = UserModel.query.filter_by(username='admin').first()
        #Combined(UserModel, anmo_rest).to_dict(joined_table)

    else:
        print("command not supported!")