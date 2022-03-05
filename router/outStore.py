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
from router.Status import Success, NotFound,NotUnique,DBError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt import JWT, jwt_required, current_identity
from router.User import UserAuth


class Outstore(Resource):
    # @jwt_required()
    def get(self, id):
        result = OutstoreModel.query.filter_by(id=id).first()

        if result:
            return result.to_dict()
        return NotFound.message, NotFound.code

    def delete(self, id):
        try:
            Outstore = OutstoreModel.query.filter_by(id=id).first()
            db.session.delete(Outstore)
        #db.session.commit()
            db.session.commit()
        except IntegrityError as e:
            print(e)
            return NotUnique.message, NotUnique.code
        except SQLAlchemyError as e: 
            print(e)
            return DBError.message, DBError.code
        return Success.message, Success.code





class OutstoreList(Resource):
    @jwt_required()
    def get(self):
        username = current_identity.to_dict()['username']
        u_auth = UserAuth().getUserAuth(username)
        conditions = []
        if(u_auth != 'adminAll'):
            conditions.append(OutstoreModel.create_name == username)
        results = OutstoreModel.query.filter(*conditions).join(ProgramModel,OutstoreModel.order_number == ProgramModel.order_number).\
        with_entities(OutstoreModel.id,OutstoreModel.is_num,OutstoreModel.is_type,OutstoreModel.order_number,ProgramModel.pro_name,OutstoreModel.out_date,OutstoreModel.out_name).order_by(OutstoreModel.out_date.desc()).all()
        response_data = [dict(zip(result.keys(), result)) for result in results]
        return {'data': response_data}

    @jwt_required()
    def post(self):
        username = current_identity.to_dict()['username']
        # print(json.load(request.json))
        Outstore = OutstoreModel()
   
        Outstore = Outstore.from_dict(request.json)
        Outstore.create_name = username
        try:
            db.session.add(Outstore)
        #db.session.commit()
            db.session.commit()
        except IntegrityError as e:
            print(e)
            return NotUnique.message, NotUnique.code
        except SQLAlchemyError as e: 
            print(e)
            return DBError.message, DBError.code
        #新建入库申请
        # data = db.session.query(ProgramModel.create_name).join(OutstoreModel,OutstoreModel.order_number == ProgramModel.order_number).first()
        # data = dict(zip(data.keys(), data))
        # MessageList().newMeassge(0,Outstore.create_name,data['create_name'])
        return Outstore.id, Success.code

    def put(self):
        pro_name = request.json['id']
        try:    
            Outstore = OutstoreModel.query.filter_by(id=id).first()
            Outstore = Outstore.from_dict(request.json)
        #db.session.commit()
            db.session.commit()
        except IntegrityError as e:
            print(e)
            return NotUnique.message, NotUnique.code
        except SQLAlchemyError as e: 
            print(e)
            return DBError.message, DBError.code
        return Success.message, Success.code


