from flask_restful import Resource
from flask import Flask, jsonify, abort, request
from models.user import User as UserModel
from models.db import db

class User(Resource):
    def get(self, user_id):
        user = UserModel.query.filter_by(username='admin').first()
        return {'user_id': user.id, 
                'user_name': user.username, 
                'email':  user.email}

        
