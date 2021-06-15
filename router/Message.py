# encoding:UTF-8

from flask_restful import Resource
from flask import Flask, jsonify, abort, request
from models.project import Project as ProjectModel
from models.Message import Message as MessageModel
from models.MessageTXT import Messagetxt as MessagetxtModel
import json
import datetime
from models.db import db
from router.Status import Success, NotFound,NotUnique,DBError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt import JWT, jwt_required, current_identity
from models.db import app


class Message(Resource):
    @jwt_required()
    def get(self):
        username = current_identity.to_dict()['username']
        print(username)
        # project = ProjectModel.query.filter_by(pro_name=pro_name).first()
        # if project:
        #     return project.to_dict()
        # return NotFound.message, NotFound.code

    def put(self):
        message_id = request.json['message_id']
        MessageModel.query.filter(MessageModel.message_id == message_id).update({
            "message_satus":1
        })
        #db.session.commit()
        try:
            db.session.commit()
        except IntegrityError as e:
            print(e)
            return NotUnique.message, NotUnique.code
        except SQLAlchemyError as e: 
            print(e)
            return DBError.message, DBError.code
        return Success.message, Success.code

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)

class MessageList(Resource):
    @jwt_required()
    def get(self):
        username = current_identity.to_dict()['username']
        print(username)
        messages =  MessageModel.query.filter(
            MessageModel.recipient_name == username).filter(MessageModel.message_satus == 0).join(MessagetxtModel,MessagetxtModel.message_type == MessageModel.message_type).with_entities(MessageModel.message_id,MessageModel.recipient_name,MessagetxtModel.message_notes,MessageModel.message_satus,MessageModel.create_name,MessageModel.create_at).all()
        response_data = [dict(zip(result.keys(), result)) for result in messages]
        count = len(response_data)
        str = json.dumps(response_data, cls=DateEncoder)
        result = json.loads(str)
        return {'data': result,
                'count': count}
        # return {'data': [user.to_dict() for user in ProjectModel.query.filter_by(is_delete = False).all()]}

    def newMeassge(self, type, c_name, r_name):

        # print(json.load(request.json))
        message = MessageModel()
      
        message.create_name = c_name
        message.recipient_name = r_name
        message.message_type = type
        message.message_satus = 0
        # if type == 0:
        #     message.message_notes = '您有一条入库申请'
        # elif type == 1:
        #     message.message_notes = '您有一条出库申请'
        # elif type == 5:
        #      message.message_notes = '您有一条入库申请通过消息' 
        # elif type == 6:
        #      message.message_notes = '您有一条入库申请驳回消息'                
        db.session.add(message)
        #db.session.commit()
        try:
            db.session.commit()
        except IntegrityError as e:
            print(e)
            return NotUnique.message, NotUnique.code
        except SQLAlchemyError as e: 
            print(e)
            return DBError.message, DBError.code
        return Success.message, Success.code


