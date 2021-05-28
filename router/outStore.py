# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import Flask, jsonify, abort, request
from models.program import Program as ProgramModel
from models.project import Project as ProjectModel
from models.outStore import outStore as OutstoreModel
from router.Message import MessageList

from models import Combined
from models.db import app

from models.db import db
from router.Status import Success, NotFound
from flask_jwt import JWT, jwt_required, current_identity


class Outstore(Resource):
    # @jwt_required()
    def get(self, id):
        result = OutstoreModel.query.filter_by(id=id).first()

        if result:
            return result.to_dict()
        return NotFound.message, NotFound.code

    def delete(self, id):
        Outstore = OutstoreModel.query.filter_by(id=id).first()
        db.session.delete(Outstore)
        db.session.commit()
        return Success.message, Success.code





class OutstoreList(Resource):
    @jwt_required()
    def get(self):
        username = current_identity.to_dict()['username']
        results = OutstoreModel.query.filter(OutstoreModel.create_name == username).join(ProgramModel,OutstoreModel.order_number == ProgramModel.order_number).\
        with_entities(OutstoreModel.id,OutstoreModel.is_num,OutstoreModel.is_status,OutstoreModel.is_type,OutstoreModel.location,OutstoreModel.order_number,OutstoreModel.in_store_num,OutstoreModel.check_name,OutstoreModel.check_time,OutstoreModel.check_form_id,ProgramModel.pro_name,OutstoreModel.in_date,OutstoreModel.store_name,ProgramModel.task_name_book).order_by(OutstoreModel.in_date.desc()).all()
        response_data = [dict(zip(result.keys(), result)) for result in results]
        return {'data': response_data}

    @jwt_required()
    def post(self):
        username = current_identity.to_dict()['username']
        # print(json.load(request.json))
        Outstore = OutstoreModel()
        print(username)
        Outstore = Outstore.from_dict(request.json)
        Outstore.create_name = username
        db.session.add(Outstore)
        db.session.commit()
        #新建入库申请
        data = db.session.query(ProgramModel.create_name).join(OutstoreModel,OutstoreModel.order_number == ProgramModel.order_number).first()
        data = dict(zip(data.keys(), data))
        MessageList().newMeassge(0,Outstore.create_name,data['create_name'])
        return Success.message, Success.code

    def put(self):
        pro_name = request.json['id']
        Outstore = OutstoreModel.query.filter_by(id=id).first()
        Outstore = Outstore.from_dict(request.json)
        db.session.commit()
        return Success.message, Success.code


@app.route('/confirmOutstore/<order_number>')
def getConfirm(order_number):

    u = db.session.query(OutstoreModel).filter(
        OutstoreModel.order_number == order_number).filter(OutstoreModel.is_status == 0).all()
    result = [data.to_dict() for data in u]
    return {'data': result}


@app.route('/confirmOutstore', methods=['POST'])

@jwt_required()
def confirmStore():
    username = current_identity.to_dict()['username']
    value = {}
    value['order_number'] = request.json['order_number']
    value['id'] = request.json['id']

    #value['is_num'] = request.json['is_num'] 不改变入库数量 
    value['is_status'] = request.json['status'] #审核状态
    value['check_name'] = request.json['check_name']
    value['check_time'] = request.json['check_time']
    if value['is_status'] == 1: #申请入库成功
        value['sign_check_form_id'] = request.json['sign_check_form_id']
    OutstoreModel.query.filter_by(order_number=request.json['order_number'], id=request.json['id']).update(value)
    
    db.session.commit()

    #new a 入库申请通过/驳回
    data = db.session.query(OutstoreModel.create_name).filter_by(order_number=request.json['order_number'], id=request.json['id']).first()
    data = dict(zip(data.keys(), data))
    print (data)
    if  value['is_status'] == 1:

        MessageList().newMeassge(5,username,data['create_name'])
    elif  value['is_status'] == 2:
        MessageList().newMeassge(6,username,data['create_name'])

    return 'Update %s store successfully' % request.json['order_number']
