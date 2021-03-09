from flask_restful import Resource
from flask import Flask, jsonify, abort, request
from models.program import Program as ProgramModel
from models.project import Project as ProjectModel
from models.instore import Instore as InstoreModel

from models import Combined
from models.db import db
from router.Status import Success, NotFound
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.sql import func


class Program(Resource):
    # @jwt_required()
    def get(self, task_id):
        # print(current_identity)
        #joined_table = db.session.query(ProgramModel, ProjectModel,func.sum(InstoreModel.is_num-InstoreModel.in_store_num).label('w_sum')).outerjoin(ProjectModel).outerjoin(InstoreModel,InstoreModel.program_code == ProgramModel.program_code).filter(ProgramModel.task_id==task_id).group_by(ProgramModel, ProjectModel)
        # print(joined_table)
        #data = [dict(zip(result.keys(), result)) for result in joined_table]
        # print(data)
        #result = Combined(ProgramModel, ProjectModel,{"sum":0}).exclude(['id'], ['id']).to_dict(joined_table)
        # sql =
        data = db.session.execute(
             'SELECT * FROM PROGRAM_VIEW WHERE TASK_ID = (:id)', {"id":task_id}
        ).fetchone()
        #print(data)
        result = dict(zip(data.keys(), data))
        if result:
            return result
        return NotFound.message, NotFound.code

    def delete(self, task_id):
        program = ProgramModel.query.filter_by(task_id=task_id).first()
        db.session.delete(program)
        db.session.commit()
        return Success.message, Success.code


class ProgramList(Resource):

    def get(self):
        #instore_table = db.session.query(InstoreModel.program_code,func.sum(InstoreModel.is_num).label('sum')).group_by(InstoreModel.program_code).all()
        #print (type(instore_table))
        #data = [dict(zip(result.keys(), result)) for result in instore_table]

        #joined_table = db.session.query(ProgramModel, func.sum(InstoreModel.is_num-InstoreModel.in_store_num).label(
            #'w_sum')).outerjoin(InstoreModel, InstoreModel.program_code == ProgramModel.program_code).group_by(ProgramModel).all()
        #joined_table = joined_table.query()
        #print((joined_table))
        # test1
        # result = Combined(
        #     ProgramModel, InstoreModel.is_num).to_dict(joined_table)
        data = db.session.execute(
             'SELECT * FROM PROGRAM_VIEW '
        ).fetchall()
        
        results = [dict(zip(result.keys(), result)) for result in data]
        print(results)
        # if programs:
       
        return {'data': results}



       

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
