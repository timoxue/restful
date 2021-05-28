from flask_restful import Resource
from flask import Flask, jsonify, abort, request
from models.program import Program as ProgramModel
from models.project import Project as ProjectModel
from models.instore import Instore as InstoreModel
from models.db import app

from models import Combined
from models.db import db
from router.Status import Success, NotFound
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.sql import func
import json
import datetime
import decimal
from models.db import app


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
            'SELECT * FROM PROGRAM_VIEW WHERE TASK_ID = (:id)', {"id": task_id}
        ).fetchone()
        # print(data)
        result = dict(zip(data.keys(), data))
        if result:
            return result
        return NotFound.message, NotFound.code

    def delete(self, task_id):
        program = ProgramModel.query.filter_by(task_id=task_id).first()
        db.session.delete(program)
        db.session.commit()
        return Success.message, Success.code


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)


class ProgramList(Resource):
    @jwt_required()
    def get(self):
        username = current_identity.to_dict()['username']
        #instore_table = db.session.query(InstoreModel.program_code,func.sum(InstoreModel.is_num).label('sum')).group_by(InstoreModel.program_code).all()
        #print (type(instore_table))
        #data = [dict(zip(result.keys(), result)) for result in instore_table]

        # joined_table = db.session.query(ProgramModel, func.sum(InstoreModel.is_num-InstoreModel.in_store_num).label(
        # 'w_sum')).outerjoin(InstoreModel, InstoreModel.program_code == ProgramModel.program_code).group_by(ProgramModel).all()
        #joined_table = joined_table.query()
        # print((joined_table))
        # test1
        # result = Combined(
        #     ProgramModel, InstoreModel.is_num).to_dict(joined_table)
        data = db.session.execute(
            'SELECT * FROM sfincident.PROGRAM_VIEW WHERE RES_NAME = (:USER) ORDER BY create_time DESC', {
                "USER": username}
        ).fetchall()

        results = [dict(zip(result.keys(), result)) for result in data]
        print(results)
        str = json.dumps(results, cls=DateEncoder)
        result = json.loads(str)
        return {'data': result}

    @jwt_required()
    def post(self):

        # print(json.load(request.json))
        username = current_identity.to_dict()['username']
        program = ProgramModel()
        program = program.from_dict(request.json)
        program.create_name = username
        db.session.add(program)
        db.session.commit()
        return Success.message, Success.code

    def put(self):
        pro_name = request.json['pro_name']
        program = ProgramModel.query.filter_by(pro_name=pro_name).first()
        program = program.from_dict(request.json)
        db.session.commit()
        return Success.message, Success.code


@app.route('/selectPrograms')
def programsParameters():
    programs = [data.to_dict() for data in ProgramModel.query.all()]
    data = []
    obj = {
    }
    for r in programs:
        obj = {}
        obj['order_number'] = r['order_number']
        obj['program_code'] = r['program_code']
        data.append(obj)

    return {'data': data}

@app.route('/programProcess')
def programProcess():
    data = db.session.execute(
            'SELECT * FROM sfincident.PROGRAM_PROCESS ORDER BY percent DESC limit 10').fetchall()

    results = [dict(zip(result.keys(), result)) for result in data]
    print(results)
    str = json.dumps(results, cls=DateEncoder)
    result = json.loads(str)
    return {'data': result}