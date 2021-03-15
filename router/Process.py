# encoding:UTF-8 

from flask_restful import Resource, Api, reqparse
from flask import Flask, jsonify, abort, request
from models.Process import Process as ProcessModel
from models.Incident import Incident as IncidentModel
from models.Component import Component as ComponentModel
from models.program import Program as ProgramModel
from models.project import Project as ProjectModel
from models.db import db
from models.db import app
from flask_jwt import JWT, jwt_required, current_identity

from router.Status import Success, NotFound
import datetime

class ProcessList(Resource):
    @jwt_required()
    def get(self):
        username = current_identity.to_dict()['username']
        conditions = []
        parser = reqparse.RequestParser()
        role_type = parser.add_argument('role_type')
        if role_type == 'process_owner':
            conditions.append(ProcessModel.process_owner == username)
        if role_type == "experimenter":
            conditions.append(ProcessModel.experimenter == username)

        args = parser.parse_args()
        results = ProcessModel.query.filter(*conditions).filter(ProcessModel.process_status != 0).join(IncidentModel, IncidentModel.incident_id==ProcessModel.incident_id). \
        join(ProgramModel, ProgramModel.order_number==IncidentModel.order_number).\
        join(ProjectModel, ProjectModel.id==ProgramModel.pro_id).\
        with_entities(ProgramModel.pro_name, ProgramModel.pro_id,
                ProjectModel.finish_time,
                IncidentModel.incident_id, IncidentModel.create_name,IncidentModel.order_number, IncidentModel.experi_project, IncidentModel.experi_type,
                ProcessModel.process_id, ProcessModel.process_name, ProcessModel.start_time_d, ProcessModel.end_time_d, ProcessModel.process_name,ProcessModel.process_status, ProcessModel.experimenter).all()
        #incidents = [incident.to_dict() for incident in IncidentModel.query.filter_by(IncidentModel.process_status==args['process_status']).all()]
        print(results)
        response_data = [dict(zip(result.keys(), result)) for result in results]
        for entity in response_data:
                entity['start_time_d'] = datetime.datetime.strftime(entity['start_time_d'], '%Y-%m-%d %H:%M:%S')
                entity['end_time_d'] = datetime.datetime.strftime(entity['end_time_d'], '%Y-%m-%d %H:%M:%S')
  
        return {'data':response_data}

class ProcessStatus(Resource):
    def put(self):
        req_data = request.json
        value = {}
        process_id = req_data['process_id']
        value['process_status'] = req_data['process_status'] 
        # if  req_data['experimenter']:
        #     value['experimenter'] = req_data['experimenter']
        #del req_data['process_id']
        #del req_data['create_at']
        #del req_data['update_at']
        if "start_time_d" in req_data.keys():
                value['start_time_d'] = datetime.datetime.strptime(req_data['start_time_d'].encode('utf-8'), '%Y-%m-%d %H:%M:%S')
        if "end_time_d" in req_data.keys():
                value['end_time_d'] = datetime.datetime.strptime(req_data['end_time_d'].encode('utf-8'), '%Y-%m-%d %H:%M:%S')
        ProcessModel.query.filter(ProcessModel.process_id==process_id).update(value)
        db.session.commit()
        return Success.message, Success.code

class CheckProcessStatus(Resource):
    def post(self):
        req_data = request.json
        process_id = req_data['process_id']
        current_process = ProcessModel.query.filter_by(ProcessModel.process_id==process_id).first()
        next_process_id = current_process.pos_process_id
        incdient_id = current_process.incdient_id
        if not next_process_id:
            ProcessModel.query.filter(ProcessModel.process_id==process_id).update({'process_status': 4}) 
            ProcessModel.query.filter(ProcessModel.process_id==next_process_id).update({'process_status': 1}) 
            ComponentModel.query.filter(ComponentModel.process_id==process_id).update({'component_status1':1, 'process_id': next_process_id})
        else:
            ProcessModel.query.filter(ProcessModel.process_id==process_id).update({'process_status': 4}) 
            IncidentModel.query.filter(IncidentModel.incident_id==incdient_id).update({'incident_status': 2})
            ComponentModel.query.filter(ComponentModel.process_id==process_id).update({'component_status1':3})

        return Success.message, Success.code

@app.route('/getOverviewProStatus')
@jwt_required()
def overviewStatus():
    username = current_identity.to_dict()['username']
    req_data = request.json
    conditions = []
    parser = reqparse.RequestParser()    
    role_type = parser.add_argument('role_type')
    if role_type == 'process_owner':
        conditions.append(ProcessModel.process_owner == username)
    if role_type == "experimenter":
        conditions.append(ProcessModel.experimenter == username)

    allIncident = ProcessModel.query.filter(*conditions).count() #分配给自己的工序
    finishIncident = ProcessModel.query.filter(*conditions).filter(ProcessModel.process_status == 4).count()
    assginIncident = ProcessModel.query.filter(*conditions).filter(ProcessModel.process_status == 2).count() #已分配和待领取
    processIncident = ProcessModel.query.filter(*conditions).filter(ProcessModel.process_status == 3).count()
    unassginIncident =  ProcessModel.query.filter(*conditions).filter(ProcessModel.process_status == 1).count()#待分配
    data = {
        "allIncident":allIncident,
        "finishIncident":finishIncident,
        "assginIncident":assginIncident,
        "processIncident":processIncident,
        "unassginIncident":unassginIncident

    }
    return data