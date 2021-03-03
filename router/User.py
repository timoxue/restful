# encoding:UTF-8 
from flask_restful import Resource
from flask import Flask, jsonify, abort, request
from models.user import User as UserModel
#from models.user import UserModel
from models.db import db


class User(Resource):
    def get(self, user_id):
        user = UserModel.query.filter_by(username=user_id).first()
        if user:
            return user.json()
        return {'message': 'User not found'}, 404



class UserList(Resource):
    def get(self):

        return {'users': [user.json() for user in UserModel.query.all()]}
    
    def post(self):
           
        # 查询该国家是否存在于数据库中
            name = request.json['username']
            u_id =  request.json['u_id']
            #udata = request.get_json()
           
            user = UserModel(username = name,u_id = u_id)
            print(user)
            db.session.add(user)
            db.session.commit()
