from flask_restful import Resource, Api, reqparse
from flask import Flask, jsonify, abort, request
from models.Incident import Incident as IncidentModel
from models.Component import Component as ComponentModel
from models.program import Program as ProgramModel
from models.project import Project as ProjectModel
from models.Process import Process as ProcessModel
from models.db import app

from models.db import db
from router.Status import Success, NotFound
import datetime


class Component(Resource):
    def post(self):
        db.session.execute(
            ComponentModel.__table__.insert(),
            request.json['data']
        )
        db.session.commit()
        return Success.message, Success.code


@app.route('/addExComponent/<order_number>')
def addExComponent(order_number):

    u = db.session.query(ComponentModel).filter(
        ComponentModel.order_number == order_number).filter(ComponentModel.component_status == 1).filter(ComponentModel.component_status1 == 0).all()
    #print ((u))
    result = [data.to_dict() for data in u]
    return {'data': result}

class ComponentList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('process_id', type=int)
        parser.add_argument('process_status', type=int)
        args = parser.parse_args()
        response_data = {}

        #1. Get current process
        dis_process = ProcessModel.query.filter(ProcessModel.process_id==args['process_id']) \
                    .join(IncidentModel.incident_id==ProcessModel.incident_id) \
                    .join(ProgramModel, ProgramModel.order_number==IncidentModel.order_number) \
                    .join(ProjectModel, ProjectModel.id==ProgramModel.pro_id) \
                    .with_entities(ProgramModel.pro_name, ProgramModel.pro_id,
                            ProjectModel.finish_time,
                            IncidentModel.incident_id, IncidentModel.create_name, 
                            ProcessModel.process_id, ProcessModel.process_name, 
                            ProcessModel.start_time_d, ProcessModel.end_time_d, 
                            ProcessModel.process_name,ProcessModel.process_status, ProcessModel.experimenter).first()
        response_data = [dict(zip(result.keys(), result)) for result in dis_process]
        for entity in response_data:
                entity['start_time_d'] = datetime.datetime.strftime(entity['start_time_d'], '%Y-%m-%d %H:%M:%S')
                entity['end_time_d'] = datetime.datetime.strftime(entity['end_time_d'], '%Y-%m-%d %H:%M:%S')
  
        #2 Get group process under the same incident
        group_incident_id = dis_process.incident_id
        group_processes = ProcessModel.query.filter(ProcessModel.incident_id==group_incident_id).order_by(ProcessModel.step_number).all()
        co_workers = set()
        group_processes_names =[]
        for g_p in group_processes:
            co_workers.add(g_p.process_owner)
            group_processes_names.append(g_p.process_name)
        response_data["co_experimenter"] = list(co_workers)
        response_data["processes"] = group_processes_names

        #3 get group Components
        group_components = ComponentModel.query.filter(ComponentModel.process_id==args['process_id']) \
                            .all()
        components_data = [dict(zip(result.keys(), result)) for result in group_components]
        del components_data['create_at']
        del components_data['update_at']
        #4 update return data
        response_data.update(components_data)

        return {'data':response_data}
