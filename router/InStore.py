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
from router.Status import Success, NotFound,NotUnique,DBError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
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

    def put(self,id):
        instore = InstoreModel.query.filter_by(id = id).first()
        is_num = request.json['instore'] + instore.in_store_num
        #is_num = instore.is_num
        #正式入库
        InstoreModel.query.filter(InstoreModel.id == id).update({"in_store_num":is_num})
        db.session.commit()
        return Success.message, Success.code

    def checkInstoreType(self,id):
        instore = InstoreModel.query.filter_by(id = id).first()
        return instore.is_type

class InstoreList(Resource):
    @jwt_required()
    def get(self):
        username = current_identity.to_dict()['username']
        results = InstoreModel.query.filter(InstoreModel.create_name == username).join(ProgramModel,InstoreModel.order_number == ProgramModel.order_number).\
        with_entities(InstoreModel.id,InstoreModel.is_num,InstoreModel.is_status,InstoreModel.is_type,InstoreModel.location,InstoreModel.order_number,InstoreModel.in_store_num,InstoreModel.check_name,InstoreModel.check_time,InstoreModel.check_form_id,ProgramModel.pro_name,InstoreModel.in_date,InstoreModel.store_name,ProgramModel.task_name_book).order_by(InstoreModel.in_date.desc()).all()
        response_data = [dict(zip(result.keys(), result)) for result in results]
        return {'data': response_data}

    @jwt_required()
    def post(self):
        username = current_identity.to_dict()['username']
        # print(json.load(request.json))
        instore = InstoreModel()
        print(username)
        instore = instore.from_dict(request.json)
        instore.create_name = username
        try:
            db.session.add(instore)
        #db.session.commit()
        
            db.session.commit()
        except IntegrityError as e:
            print(e)
            return NotUnique.message, NotUnique.code
        except SQLAlchemyError as e: 
            print(e)
            return DBError.message, DBError.code
        #新建入库申请
        data = db.session.query(ProgramModel.create_name).join(InstoreModel,InstoreModel.order_number == ProgramModel.order_number).first()
        data = dict(zip(data.keys(), data))
        MessageList().newMeassge(0,instore.create_name,data['create_name'])
        return Success.message, Success.code

    def put(self):
        pro_name = request.json['id']
        try:
            instore = InstoreModel.query.filter_by(id=id).first()
            instore = instore.from_dict(request.json)
        #db.session.commit()
        
            db.session.commit()
        except IntegrityError as e:
            print(e)
            return NotUnique.message, NotUnique.code
        except SQLAlchemyError as e: 
            print(e)
            return DBError.message, DBError.code
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
    value = {}
    value['order_number'] = request.json['order_number']
    value['id'] = request.json['id']

    #value['is_num'] = request.json['is_num'] 不改变入库数量 
    value['is_status'] = request.json['status'] #审核状态
    value['check_name'] = request.json['check_name']
    value['check_time'] = request.json['check_time']
    if value['is_status'] == 1: #申请入库成功
        value['sign_check_form_id'] = request.json['sign_check_form_id']
    try:
        InstoreModel.query.filter_by(order_number=request.json['order_number'], id=request.json['id']).update(value)
    
    #db.session.commit()

        db.session.commit()
    except IntegrityError as e:
        print(e)
        return NotUnique.message, NotUnique.code
    except SQLAlchemyError as e: 
        print(e)
        return DBError.message, DBError.code

    #new a 入库申请通过/驳回
    data = db.session.query(InstoreModel.create_name).filter_by(order_number=request.json['order_number'], id=request.json['id']).first()
    data = dict(zip(data.keys(), data))
    print (data)
    if  value['is_status'] == 1:

        MessageList().newMeassge(5,username,data['create_name'])
    elif  value['is_status'] == 2:
        MessageList().newMeassge(6,username,data['create_name'])

    return 'Update %s store successfully' % request.json['order_number']
