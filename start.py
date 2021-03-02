from flask import Flask, request
from flask_restful import Resource, Api
from router.HelloWord import HelloWorld
from router.User import User
from models.db import app

api = Api(app)

api.add_resource(HelloWorld, '/')
api.add_resource(User, '/user/<string:user_id>')


if __name__ == '__main__':
    app.run(debug=False)