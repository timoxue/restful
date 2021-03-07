from flask_restful import Resource
from flask import Flask, jsonify, abort, request
from models.program import Program as ProgramModel
from models.project import Project as ProjectModel

from models.db import db
from router.Status import Success, NotFound
from flask_jwt import JWT, jwt_required, current_identity


class Program(Resource):
    @jwt_required()
    def get(self, task_id):
        print(current_identity)
        program = ProgramModel.query.filter_by(task_id=task_id).first()
        if program:
            return program.to_dict()
        return NotFound.message, NotFound.code

    def delete(self, task_id):
        program = ProgramModel.query.filter_by(task_id=task_id).first()
        db.session.delete(program)
        db.session.commit()
        return Success.message, Success.code


class ProgramList(Resource):
    def get(self):

        #programs = ProgramModel.query.join(ProjectModel, ProgramModel.pro_id == ProjectModel.id).all()
        programs = db.session.query(ProgramModel,ProjectModel).outerjoin(ProjectModel).filter(ProgramModel.pro_id == ProjectModel.id)
        result = db.session.execute(programs).fetchall()
        #programs = [program.to_dict() for program in ProgramModel.query
        #              .outerjoin(ProjectModel, ProgramModel.pro_id == ProjectModel.id).add_entity(ProjectModel)]
        #print (programs)
        #result = db.session.execute(programs)
        print (result)
        #result = [program.to_dict() for program in programs]
        #if programs:
            #return {'data': result}
        
        # for user in users:
        #     for k in list(user.keys()):
        #         #print (k)
        #         if(k == 'is_delete' or k == 'u_password'):
        #             del user[k]
        
        # return {'data': [user.to_dict() for user in ProgramModel.query.filter_by(is_delete = False).all()]}

    def post(self):
        # print(json.load(request.json))
        program = ProgramModel()
        program = program.from_dict(request.json)

        db.session.add(program)
        db.session.commit()
        return Success.message, Success.code

    def put(self):
        pro_name = request.json['pro_name']
        program = ProgramModel.query.filter_by(pro_name=pro_name).first()
        program = program.from_dict(request.json)
        db.session.commit()
        return Success.message, Success.code
