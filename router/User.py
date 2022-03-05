# encoding:UTF-8
from flask_restful import Resource
from flask import Flask, jsonify, abort, request
from models.user import User as UserModel
from models.db import db
from router.Status import Success, NotFound,NotUnique,DBError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt import JWT, jwt_required, current_identity
from models.db import app
class User(Resource):
    #@jwt_required()
    def get(self, user_id):
        print(UserModel)
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


@app.route('/checkUserID/<USER_ID>')
def checkUser(USER_ID):
    count = UserModel.query.filter_by(u_id = USER_ID).count()
    print(count)
    if count == 0:
       
        return Success.message, Success.code
    else: 
        return {'message': '重复用户工号'},500

@app.route('/checkUserName/<USER_NAME>')
def checkName(USER_NAME):
    count = UserModel.query.filter_by(username = USER_NAME).count()
    print(count)
    if count == 0:
        return Success.message, Success.code
    else: 
        return {'message': '重复用户账号'},500

@app.route('/updateUsers' ,methods=['PUT'])
def updateUsers():
    request_data = request.json
    value = {
        'u_authority':request_data['u_authority'],
        'u_department':request_data['u_department'],
        'u_email':request_data['u_email'],
        'u_name':request_data['u_name'],
        'u_tele':request_data['u_tele'],
        'u_id':request_data['u_id']
    }
    username = request_data['username']
    try:
        UserModel.query.filter_by(username=username).update(value)
        db.session.commit()
    except IntegrityError as e:
        print(e)
        return NotUnique.message, NotUnique.code
    except SQLAlchemyError as e: 
        print(e)
        return DBError.message, DBError.code
    return Success.message, Success.code    

class UserAuth(Resource):
    def getUserAuth(self,u_name):
        u = UserModel.query.filter_by(username = u_name).first()
        return u.u_authority

