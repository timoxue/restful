from flask_restful import Resource
from flask import Flask, jsonify, abort, request
from models.user import User as UserModel
#from models.user import UserModel
from models.db import db
from router.Status import Success, NotFound

class User(Resource):
    def get(self, user_id):
        user = UserModel.query.filter_by(username=user_id).first()
        if user:
            return user.to_dict()
        return NotFound.message, NotFound.code

    def delete(self, user_id):
        user = UserModel.query.filter_by(username=user_id).first()
        db.session.delete(user)
        db.session.commit()
        return Success.message, Success.code


class UserList(Resource):
    def get(self):
        
        users = [user.to_dict() for user in UserModel.query.filter_by(is_delete = False).all()]
        for user in users:
            for k in list(user.keys()):
                #print (k)
                if(k == 'is_delete' or k == 'u_password'):  
                    del user[k]
        return {'data':users}
        #return {'data': [user.to_dict() for user in UserModel.query.filter_by(is_delete = False).all()]}
    
    def post(self):
        #print(json.load(request.json))
        user = UserModel()
        user = user.from_dict(request.json)
        
        db.session.add(user)
        db.session.commit()
        return Success.message, Success.code

    def put (self):
        username = request.json['username']
        user = UserModel.query.filter_by(username=username).first()
        user = user.from_dict(request.json)
        db.session.commit()
        return Success.message, Success.code

