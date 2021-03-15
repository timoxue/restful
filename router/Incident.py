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
from sqlalchemy import or_
from flask_jwt import JWT, jwt_required, current_identity
from router.Message import MessageList


from router.Status import Success, NotFound
import datetime

class Incident(Resource):
    def get(self):
        result = [incident.to_dict() for incident in IncidentModel.query.all()]
        return {'data': result}

    @jwt_required()
    def post(self):
        username = current_identity.to_dict()['username']
        req_data = request.json

        req_data['create_name'] = username
      #1. get process list and component_list
        component_list = req_data['component_list']
        process_list = req_data['process_list']
        req_data['create_user'] = "test"

        #2. get component list

        #3. remove the process list and component_list in the orginal json
        del req_data['process_list']
        del req_data['component_list']
          
        #4. insert into incident table 
        incident = IncidentModel()
        incident = incident.from_dict(req_data)
        #更改incident状态为已创建
        incident.incident_status = 0
        db.session.add(incident)
        db.session.commit()

        #5. update insert into process table
        list_l = len(process_list)
        update_process_list = []
        for i in range(list_l):
            process_list[i]['incident_id'] = incident.incident_id
            process_list[i]['experiment_owner'] = username
            if process_list[i]['step_number'] == 0:
                #第一个工序的状态默认为待分配
                process_list[i]['process_status'] = 1
                #取第一个工序负责人，并向其发消息
                recipient_name = process_list[i]['process_owner']
            else:
                process_list[i]['process_status'] = 0
            p = ProcessModel().from_dict(process_list[i])
            db.session.add(p)
            db.session.commit()
            update_process_list.append(p)

        for i in range(list_l):
            if i == list_l-1:
                update_process_list[i].pre_process_id = update_process_list[i-1].process_id
            elif i == 0:
                update_process_list[i].pos_process_id = update_process_list[i+1].process_id
            else:
                update_process_list[i].pre_process_id = update_process_list[i-1].process_id
                update_process_list[i].pos_process_id = update_process_list[i+1].process_id

        for i in range(list_l):
            value = {}
            value['process_id'] = update_process_list[i].process_id
            if i == list_l-1:
                value['pre_process_id'] = update_process_list[i-1].process_id
                value['pos_process_id'] = None
            elif i == 0:
                value['pre_process_id'] = None
                value['pos_process_id'] = update_process_list[i+1].process_id
            else:
                value['pre_process_id'] = update_process_list[i-1].process_id
                value['pos_process_id'] = update_process_list[i+1].process_id
            ProcessModel.query.filter(ProcessModel.process_id==value['process_id']).update({'pre_process_id': value['pre_process_id'],'pos_process_id': value['pos_process_id']})
            db.session.commit()

        #6. update insert into Component table

        for i, _ in enumerate(component_list):
            value = {}
            #value['id'] = component_list[i]['id']
            value['incident_id'] = incident.incident_id
            value['create_at'] = datetime.datetime.strptime(component_list[i]['create_at'].encode('utf-8'), '%Y-%m-%d %H:%M:%S')
            value['order_number'] = component_list[i]['order_number']
            value['original_id'] = component_list[i]['original_id']
            value['component_status'] = component_list[i]['component_status']
            #更改试验件的状态 变更为已分配
            value['component_status1'] = 1
            value['component_unique_id'] = component_list[i]['component_unique_id']
            #del component_list[i]['create_at']
            #del component_list[i]['update_at']
            ComponentModel.query.filter(ComponentModel.id==component_list[i]['id']).update(value)
            db.session.commit()

        #new message
        MessageList().newMeassge(4,username,recipient_name)

        return Success.message, Success.code





class IncidentList(Resource):
    def get(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument('incident_status', type=int)
        # args = parser.parse_args()
        results = IncidentModel.query. \
        join(ProcessModel,IncidentModel.incident_id==ProcessModel.incident_id).filter(or_(ProcessModel.process_status == 1,ProcessModel.process_status == 2,ProcessModel.process_status == 3)).\
        join(ProgramModel, ProgramModel.order_number==IncidentModel.order_number).\
        join(ProjectModel, ProjectModel.id==ProgramModel.pro_id).\
        with_entities(ProgramModel.pro_name, ProgramModel.pro_id,
                ProjectModel.finish_time,
                IncidentModel.incident_id, IncidentModel.create_name, 
                ProcessModel.process_id, ProcessModel.process_name, ProcessModel.start_time_d, ProcessModel.end_time_d, ProcessModel.process_name,ProcessModel.process_status, ProcessModel.experimenter).all()
        #incidents = [incident.to_dict() for incident in IncidentModel.query.filter_by(IncidentModel.process_status==args['process_status']).all()]

        response_data = [dict(zip(result.keys(), result)) for result in results]
        for entity in response_data:
                entity['start_time_d'] = datetime.datetime.strftime(entity['start_time_d'], '%Y-%m-%d %H:%M:%S')
                entity['end_time_d'] = datetime.datetime.strftime(entity['end_time_d'], '%Y-%m-%d %H:%M:%S')
  
        return {'data':response_data}


@app.route('/getOverviewIncStatus')
def overviewIncidentStatus():
    allIncident = IncidentModel.query.count()
    finishIncident = IncidentModel.query.filter(IncidentModel.incident_status == 2).count()
    unprocessIncident = IncidentModel.query.filter(IncidentModel.incident_status == 0).count()
    processIncident = IncidentModel.query.filter(IncidentModel.incident_status == 1).count()
    data = {
        "allIncident":allIncident,
        "finishIncident":finishIncident,
        "processIncident":processIncident,
        "unprocessIncident":unprocessIncident
    }
    return data
