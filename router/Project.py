from flask_restful import Resource
from flask import Flask, jsonify, abort, request
from models.project import Project as ProjectModel
from models.db import db
from router.Status import Success, NotFound
from flask_jwt import JWT, jwt_required, current_identity


class Project(Resource):
    @jwt_required()
    def get(self, pro_name):
        username = current_identity.to_dict()['username']
        print (username)
        project = ProjectModel.query.filter_by(pro_name=pro_name).first()
        if project:
            return project.to_dict()
        return NotFound.message, NotFound.code

    def delete(self, pro_name):
        project = ProjectModel.query.filter_by(pro_name=pro_name).first()
        db.session.delete(project)
        db.session.commit()
        return Success.message, Success.code


class ProjectList(Resource):
    @jwt_required()
    def get(self):
        username = current_identity.to_dict()['username']
        print (username)
        projects = [project.to_dict() for project in ProjectModel.query.filter(ProjectModel.create_name == username).all()]
        # for user in users:
        #     for k in list(user.keys()):
        #         #print (k)
        #         if(k == 'is_delete' or k == 'u_password'):  
        #             del user[k]
        return {'data':projects}
        #return {'data': [user.to_dict() for user in ProjectModel.query.filter_by(is_delete = False).all()]}
    
    def post(self):
        #print(json.load(request.json))
        project = ProjectModel()
        project = project.from_dict(request.json)
        
        db.session.add(project)
        db.session.commit()
        return Success.message, Success.code

    def put (self):
        pro_name = request.json['pro_name']
        project = ProjectModel.query.filter_by(pro_name=pro_name).first()
        project = project.from_dict(request.json)
        db.session.commit()
        return Success.message, Success.code

