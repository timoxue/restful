from flask_restful import Resource
from flask import Flask, jsonify, abort, request
from models.project import Project as ProjectModel
from models.db import db
from router.Status import Success, NotFound

class Project(Resource):
    def get(self, pro_name):
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
    def get(self):
        
        projects = [project.to_dict() for project in ProjectModel.query.all()]
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
