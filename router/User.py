from flask_restful import Resource
from flask import Flask, jsonify, abort, request
from models.user import User as UserModel
#from models.user import UserModel
from models.db import db
from router.Status import Success, NotFound,NotUnique,DBError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt import JWT, jwt_required, current_identity

class User(Resource):
    #@jwt_required()
    def get(self, user_id):
        user = UserModel.query.filter_by(username=user_id).first()
        if user:
            return user.to_dict()
        return NotFound.message, NotFound.code

    def delete(self, user_id):
        user = UserModel.query.filter_by(username=user_id).first()
        db.session.delete(user)
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

    def put (self,user_id):
        password = request.json['password']
        u_status = request.json['u_status']
        print (password)
        try:
            UserModel.query.filter_by(username=user_id).update({
                "u_password":password,
                "u_status":u_status
            })
        
        #db.session.commit()

            db.session.commit()
        except IntegrityError as e:
            print(e)
            return NotUnique.message, NotUnique.code
        except SQLAlchemyError as e: 
            print(e)
            return DBError.message, DBError.code
        return Success.message, Success.code    

class UserList(Resource):
    @jwt_required()
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
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            print(e)
            return NotUnique.message, NotUnique.code
        except SQLAlchemyError as e: 
            print(e)
            return DBError.message, DBError.code
        return Success.message, Success.code



