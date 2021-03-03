from flask import Flask, request
from flask_restful import Resource, Api
from router.HelloWord import HelloWorld
from router.User import User
from router.User import UserList
from models.db import app
from config import gloabl_config

import os

api = Api(app)

api.add_resource(HelloWorld, '/')
api.add_resource(User, '/user/<string:user_id>')
api.add_resource(UserList, '/users')



if __name__ == '__main__':
    app.run(debug=False)