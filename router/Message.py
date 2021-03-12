# encoding:UTF-8 

from flask_restful import Resource
from flask import Flask, jsonify, abort, request
from models.project import Project as ProjectModel
from models.Message import Message as MessageModel

from models.db import db
from router.Status import Success, NotFound
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

    def delete(self, pro_name):
        project = ProjectModel.query.filter_by(pro_name=pro_name).first()
        db.session.delete(project)
        db.session.commit()
        return Success.message, Success.code


class MessageList(Resource):
    @jwt_required()
    def get(self):
        username = current_identity.to_dict()['username']
        print(username)
        messages = [message.to_dict() for message in MessageModel.query.filter(
            MessageModel.recipient_name == username).filter(MessageModel.message_satus == 0).all()]
        count = len(messages)
        return {'data': messages,
                'count': count}
        # return {'data': [user.to_dict() for user in ProjectModel.query.filter_by(is_delete = False).all()]}

    def newMeassge(self, m_name, type, c_name, r_name):

        # print(json.load(request.json))
        message = MessageModel()
        message.message_name = m_name
        message.create_name = c_name
        message.recipient_name = r_name
        message.message_type = type
        message.message_satus = 0
        if type == 0:
            message.message_notes = '您有一条入库申请'
        db.session.add(message)
        db.session.commit()
        return Success.message, Success.code

    def put(self):
        pro_name = request.json['pro_name']
        project = ProjectModel.query.filter_by(pro_name=pro_name).first()
        project = project.from_dict(request.json)
        db.session.commit()
        return Success.message, Success.code
