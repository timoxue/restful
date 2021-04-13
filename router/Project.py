from flask_restful import Resource
from flask import Flask, jsonify, abort, request
from models.project import Project as ProjectModel
from models.db import db
from router.Status import Success, NotFound
from flask_jwt import JWT, jwt_required, current_identity
from models.db import app
from router.Message import MessageList


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
        projects = [project.to_dict() for project in ProjectModel.query.filter(ProjectModel.create_name == username).order_by(ProjectModel.create_time).all()]
     
        return {'data':projects}
        #return {'data': [user.to_dict() for user in ProjectModel.query.filter_by(is_delete = False).all()]}
    
    def post(self):
        #print(json.load(request.json))
        project = ProjectModel()
        project = project.from_dict(request.json)
        
        db.session.add(project)
        db.session.commit()

        #new message
        MessageList().newMeassge(7,project.create_name,project.res_name)


        return Success.message, Success.code

    def put (self):
        pro_name = request.json['pro_name']
        project = ProjectModel.query.filter_by(pro_name=pro_name).first()
        project = project.from_dict(request.json)
        db.session.commit()
        return Success.message, Success.code

@app.route('/getProjects')
@jwt_required()
def getProjects():
    username = current_identity.to_dict()['username']
    data = db.session.execute(
        'select * from PROGRAM_VIEW  where order_number is null and res_name = (:username)',{"username":username}
         
        ).fetchall()
    results = [dict(zip(result.keys(), result))  for result in data ]
    #projects = [data.to_dict() for data in ProjectModel.query.filter_by(res_name=username).all()]
    data = []
    obj = {}
    for r in results:
        obj = {}
        obj['key'] = r['project_id']
        obj['value'] = r['project_name']
        data.append(obj)
    return {'data': data}