# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import Flask, jsonify, abort, request
from models.program import Program as ProgramModel
from models.project import Project as ProjectModel
from models.instore import Instore as InstoreModel
from router.Message import MessageList

from models import Combined
from models.db import app

from models.db import db
from router.Status import Success, NotFound
from flask_jwt import JWT, jwt_required, current_identity


class Instore(Resource):
    # @jwt_required()
    def get(self, id):
        result = InstoreModel.query.filter_by(id=id).first()

        if result:
            return result.to_dict()
        return NotFound.message, NotFound.code

    def delete(self, id):
        instore = InstoreModel.query.filter_by(id=id).first()
        db.session.delete(instore)
        db.session.commit()
        return Success.message, Success.code


class InstoreList(Resource):
    @jwt_required()
    def get(self):
        username = current_identity.to_dict()['username']
        result = [instore.to_dict() for instore in InstoreModel.query.filter(InstoreModel.create_name == username).all()]

        return {'data': result}

    @jwt_required()
    def post(self):
        username = current_identity.to_dict()['username']
        # print(json.load(request.json))
        instore = InstoreModel()
        instore = instore.from_dict(request.json)
        instore['create_name'] = username
        db.session.add(instore)
        db.session.commit()
        #新建入库申请
        data = db.session.query(ProgramModel.create_name).join(InstoreModel,InstoreModel.order_number == ProgramModel.order_number).first()
        data = dict(zip(data.keys(), data))
        print (data)
        MessageList().newMeassge("InStore",0,instore.create_name,data['create_name'])
        return Success.message, Success.code

    def put(self):
        pro_name = request.json['id']
        instore = InstoreModel.query.filter_by(id=id).first()
        instore = instore.from_dict(request.json)
        db.session.commit()
        return Success.message, Success.code


@app.route('/confirmInstore/<order_number>')
def getConfirm(order_number):

    u = db.session.query(InstoreModel).filter(
        InstoreModel.order_number == order_number).filter(InstoreModel.is_status == 0).all()
    result = [data.to_dict() for data in u]
    return {'data': result}


@app.route('/confirmInstore', methods=['POST'])

@jwt_required()
def confirmStore():
    username = current_identity.to_dict()['username']
    order_number = request.json['order_number']
    id = request.json['id']
    is_num = request.json['is_num']
    status = request.json['status'] #审核状态
    InstoreModel.query.filter_by(order_number=order_number, id=id).update({'is_status': status,
                                                                           'in_store_num': is_num,
                                                                           'check_name': request.json['check_name'],
                                                                           'check_time': request.json['check_time']
                                                                           })
    
    db.session.commit()

    #new a 入库申请通过/驳回
    data = db.session.query(InstoreModel.create_name).filter_by(order_number=order_number, id=id).first()
    data = dict(zip(data.keys(), data))
    print (data)
    if status == 1:

        MessageList().newMeassge("InStore",5,username,data['create_name'])
    elif status == 2:
        MessageList().newMeassge("InStore",6,username,data['create_name'])

    return 'Update %s store successfully' % order_number
