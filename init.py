from models.db import db, app
from models.user import User as UserModel
from models.project import Project as ProjectModel
from models.program import Program as ProgramModel


import sys,os

if __name__ == '__main__':
    command =  sys.argv[1]
    if command == 'build':
        db.create_all()
        print('created successfully')
    elif command == 'update':
        admin = UserModel(username='admin', u_email='admin@example.com', u_id="123", u_name='what', u_password='123', u_tele = "13888888888", u_authority="jingli", u_department="admin", is_delete=False)
        #guest = UserModel(username='guest', email='guest@example.com')
        db.session.add(admin)
        #db.session.add(guest)
        db.session.commit()
    elif command == 'clean':
        db.drop_all()
    elif command == 'query':
        user = UserModel.query.filter_by(username='admin').first()
        print(user.email)
    else:
        print("command not supported!")