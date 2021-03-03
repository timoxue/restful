# encoding:UTF-8 
from flask_restful import Resource
from flask import Flask, jsonify, abort, request
from models.user import User as UserModel
#from models.user import UserModel
from models.db import db
import json
from router.Status import Success

class User(Resource):
    def get(self, user_id):
        user = UserModel.query.filter_by(username=user_id).first()
        if user:
            return user.json()
        return {'message': 'User not found'}, 404



class UserList(Resource):
    def get(self):

        return {'users': [user.to_dict() for user in UserModel.query.all()]}
    
    def post(self):
        # 查询该国家是否存在于数据库中
        #print(json.load(request.json))
        user = UserModel()
        user = user.from_dict(request.json)
        #print(user.u_email)
        db.session.add(user)
        db.session.commit()
        return Success.message, Success.code


