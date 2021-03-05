from flask import Flask, request
from flask_restful import Resource, Api
from router.HelloWord import HelloWorld
from router.User import UserList, User
from router.Project import Project, ProjectList
from router.Program import Program, ProgramList



from router.File import File
from models.db import app

api = Api(app)

api.add_resource(HelloWorld, '/')
api.add_resource(User, '/user/<string:user_id>')
api.add_resource(UserList, '/users')
api.add_resource(Project, '/project/<string:pro_name>')
api.add_resource(ProjectList, '/projects')
api.add_resource(ProgramList, '/programs')
api.add_resource(File, '/files')

if __name__ == '__main__':
    app.run(debug=False)