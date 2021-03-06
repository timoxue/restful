from flask import Flask, request
from flask_restful import Resource, Api
from router.HelloWord import HelloWorld
from router.User import UserList, User
from router.Project import Project, ProjectList
from router.Program import Program, ProgramList
from router.InStore import Instore,InstoreList
from router.Component import Component
from router.Experiment import Experiment
from router.Incident import Incident,IncidentList
from router.Process import ProcessStatus
from router.Process import ProcessList
from router.Message import MessageList
from router.Component import ComponentList
from router.Component import CheckComponent

from router.File import File
from models.db import app
from utils.security import authenticate, identity
from flask_jwt import JWT, jwt_required, current_identity
import datetime

api = Api(app)
app.secret_key = 'super_secret'
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=10)

jwt = JWT(app, authenticate, identity)

api.add_resource(HelloWorld, '/')
api.add_resource(User, '/user/<string:user_id>')
api.add_resource(UserList, '/users')
api.add_resource(Project, '/project/<string:pro_name>')
api.add_resource(ProjectList, '/projects')

api.add_resource(ProgramList, '/programs')
api.add_resource(Program, '/program/<string:task_id>')

api.add_resource(InstoreList, '/instores')
api.add_resource(Instore, '/instore/<id>')
api.add_resource(Component, '/components')
api.add_resource(Experiment, '/experiment')
api.add_resource(IncidentList, '/incidents')
api.add_resource(Incident, '/incident')

api.add_resource(ProcessList, '/get_processes')
api.add_resource(ProcessStatus, '/process_status')

api.add_resource(MessageList,'/messageList')
api.add_resource(ComponentList,'/componentList')
api.add_resource(CheckComponent, '/checkComponent')

api.add_resource(File, '/files')


                                               


if __name__ == '__main__':
    app.run(debug=False)