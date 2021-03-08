from flask_restful import Resource
from flask import Flask, jsonify, abort, request
from models.program import Program as ProgramModel
from models.project import Project as ProjectModel
from models.instore import Instore as InstoreModel
from models import Combined
from models.db import app

from models.db import db
from router.Status import Success, NotFound
from flask_jwt import JWT, jwt_required, current_identity


class Instore(Resource):
    #@jwt_required()
    def get(self, id):
        result =  InstoreModel.query.filter_by(id=id).first()
        #print(current_identity)
        # joined_table = db.session.query(, ProjectModel).outerjoin(ProjectModel).filter(ProgramModel.task_id==task_id).all()
        # result = Combined(ProgramModel, ProjectModel).exclude(['id'], ['id']).to_dict(joined_table)
        if result:
            return result.to_dict()
        return NotFound.message, NotFound.code

    def delete(self, task_id):
        instore =InstoreModel.query.filter_by(task_id=task_id).first()
        db.session.delete(instore)
        db.session.commit()
        return Success.message, Success.code


class InstoreList(Resource):

    def get(self):
        result =  [instore.to_dict() for instore in InstoreModel.query.all()]
        
        return {'data': result}

    def post(self):
        # print(json.load(request.json))
        instore =InstoreModel()
        instore = instore.from_dict(request.json)

        db.session.add(instore)
        db.session.commit()
        return Success.message, Success.code

    def put(self):
        pro_name = request.json['id']
        instore =InstoreModel.query.filter_by(id=id).first()
        instore = instore.from_dict(request.json)
        db.session.commit()
        return Success.message, Success.code

@app.route('/confirmInstore/<program_code>')
def getConfirm(program_code):
    u = InstoreModel.query.filter(program_code==program_code).all()
    result =  [data.to_dict() for data in u]
    return {'data': result}
    
@app.route('/confirmInstore/<id>/<program_code>')
def confirmStore(id,program_code):
    inStore = InstoreModel(id=id, program_code=program_code)
    inStore['is_status'] = 1
    db.session.add(inStore)
    db.session.commit()
    return 'Add %s user successfully' % program_code