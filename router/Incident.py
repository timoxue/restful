from flask_restful import Resource, Api, reqparse
from flask import Flask, jsonify, abort, request
from models.Process import Process as ProcessModel
from models.Incident import Incident as IncidentModel
from models.Component import Component as ComponentModel
from models.db import db
from models.db import app

from router.Status import Success, NotFound
import datetime

class Incident(Resource):
    def get(self):
        result = [incident.to_dict() for incident in IncidentModel.query.all()]
        return {'data': result}

    def post(self):
        req_data = request.json

        req_data['create_name'] = 'test'
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
        db.session.add(incident)
        db.session.commit()

        #5. update insert into process table
        list_l = len(process_list)
        update_process_list = []
        for i in range(list_l):
            process_list[i]['incident_id'] = incident.incident_id
            if process_list[i]['step_number'] == 0:
                #第一个工序的状态默认为待分配
                process_list[i]['process_status'] = 1
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
            value['component_status1'] = component_list[i]['component_status1']
            value['component_unique_id'] = component_list[i]['component_unique_id']
            #del component_list[i]['create_at']
            #del component_list[i]['update_at']
            ComponentModel.query.filter(ComponentModel.id==component_list[i]['id']).update(value)
            db.session.commit()

        return Success.message, Success.code



@app.route('/getOverviewStatus')
def overviewStatus():
    allIncident = ProcessModel.query.count()
    finishIncident = ProcessModel.query.filter(ProcessModel.process_status == 3).count()
    assginIncident = ProcessModel.query.filter(ProcessModel.process_status == 1).count()
    processIncident = ProcessModel.query.filter(ProcessModel.process_status == 2).count()
    data = {
        "allIncident":allIncident,
        "finishIncident":finishIncident,
        "assginIncident":assginIncident,
        "processIncident":processIncident
    }
    return data


class IncidentList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('process_status', type=int)
        args = parser.parse_args()
        incidents = [incident.to_dict() for incident in IncidentModel.query.filter_by(IncidentModel.process_status==args['process_status']).all()]
        return {'data':incidents}
