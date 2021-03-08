# -*- coding: utf-8 -*-
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
    # @jwt_required()
    def get(self, id):
        result = InstoreModel.query.filter_by(id=id).first()
        # print(current_identity)
        # joined_table = db.session.query(, ProjectModel).outerjoin(ProjectModel).filter(ProgramModel.task_id==task_id).all()
        # result = Combined(ProgramModel, ProjectModel).exclude(['id'], ['id']).to_dict(joined_table)
        if result:
            return result.to_dict()
        return NotFound.message, NotFound.code

    def delete(self, id):
        instore = InstoreModel.query.filter_by(id=id).first()
        db.session.delete(instore)
        db.session.commit()
        return Success.message, Success.code


class InstoreList(Resource):

    def get(self):
        result = [instore.to_dict() for instore in InstoreModel.query.all()]

        return {'data': result}

    def post(self):
        # print(json.load(request.json))
        instore = InstoreModel()
        instore = instore.from_dict(request.json)

        db.session.add(instore)
        db.session.commit()
        return Success.message, Success.code

    def put(self):
        pro_name = request.json['id']
        instore = InstoreModel.query.filter_by(id=id).first()
        instore = instore.from_dict(request.json)
        db.session.commit()
        return Success.message, Success.code


@app.route('/confirmInstore/<order_number>')
def getConfirm(order_number):
    u = InstoreModel.query.filter(
        order_number == order_number, InstoreModel.is_status == 0).all()
    result = [data.to_dict() for data in u]
    return {'data': result}


@app.route('/confirmInstore', methods=['POST'])
def confirmStore():
    order_number = request.json['order_number']
    id = request.json['id']
    is_num = request.json['is_num']

    InstoreModel.query.filter_by(order_number=order_number, id=id).update({'is_status': 1,
                                                                           'in_store_num': is_num,
                                                                           'check_name': request.json['check_name'],
                                                                           'check_time': request.json['check_time']
                                                                           })
    db.session.commit()
    return 'Update %s store successfully' % order_number
