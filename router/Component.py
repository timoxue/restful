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
        print(args['process_status'])
        #1. Get current process
        dis_process = ProcessModel.query.filter(ProcessModel.process_id==args['process_id']) \
                    .join(IncidentModel,IncidentModel.incident_id==ProcessModel.incident_id) \
                    .join(ProgramModel, ProgramModel.order_number==IncidentModel.order_number) \
                    .join(ProjectModel, ProjectModel.id==ProgramModel.pro_id) \
                    .with_entities(ProgramModel.pro_name, ProgramModel.pro_id,ProgramModel.order_number,ProgramModel.task_id,
                            ProjectModel.finish_time,
                            IncidentModel.incident_id, IncidentModel.create_name, IncidentModel.experi_type,
                            ProcessModel.process_id, ProcessModel.process_name, 
                            ProcessModel.start_time_d, ProcessModel.end_time_d, 
                            ProcessModel.process_name,ProcessModel.process_status,ProcessModel.experimenter,ProcessModel.process_owner).all()
        print(dis_process)
        response_data = [dict(zip(result.keys(), result)) for result in dis_process]
        
        for entity in response_data:
                entity['start_time_d'] = datetime.datetime.strftime(entity['start_time_d'], '%Y-%m-%d %H:%M:%S')
                entity['end_time_d'] = datetime.datetime.strftime(entity['end_time_d'], '%Y-%m-%d %H:%M:%S')
        response_data = response_data[0]
        #2 Get group process under the same incident
        group_incident_id = response_data['incident_id']
        group_processes = ProcessModel.query.filter(ProcessModel.incident_id==group_incident_id).order_by(ProcessModel.step_number).all()
        co_workers = set()
        group_processes_names =[]
        for g_p in group_processes:
            co_workers.add(g_p.process_owner)
            processObj = { }
            processObj['process_name'] = g_p.process_name
            processObj['process_id'] = g_p.process_id
            processObj['process_owner'] = g_p.process_owner
            group_processes_names.append(processObj)
        response_data["co_experimenter"] = list(co_workers)
        response_data["processes"] = group_processes_names

        #3 get group Components
        group_components = ComponentModel.query.filter(ComponentModel.incident_id==group_incident_id) \
                            .all()
        components_data = [result.to_dict() for result in group_components]

        for entity in components_data:
            del entity['create_at']
            del entity['update_at']
        #del components_data['create_at']
        #del components_data['update_at']
        #4 update return data
        response_data['componentlist'] = components_data
        #response_data.update(components_data)

        return {'data':response_data}
    def put(self):
        request_data = request.json
        ComponentList = request_data['data']
        for value in ComponentList:
            
            ComponentModel.query.filter(ComponentModel.component_unique_id==value['component_unique_id']).update(value)
            db.session.commit()
        return Success.message, Success.code        



class CheckComponent(Resource):
    def post(self):
        request_data = request.json
        component_list = request_data['data']
        for i, _ in enumerate(component_list):
            value = {}
            componet_id = component_list[i]['component_unique_id']
            #value['']

        component_status1 = request_data['component_status1']
        component_status = request_data['component_status']
        component_id = request_data['id']
        #check_process = request_data['check_process']

        componet = ComponentModel.query.filter(ComponentModel.id==component_id).first()

        ComponentModel.query.filter_by(ComponentModel.id==component_id).update({'component_status1': component_status1,"component_status":component_status})
        #total_num = ComponentModel.query.join(ProcessModel, ComponentModel.process_id==ProcessModel.process_id).count()
        #finished_num = ComponentModel.query.join(ProcessModel, ComponentModel.process_id==ProcessModel.process_id).filter(ComponentModel.component_status1==2).count()

        # if check_process and (total_num==finished_num):
        #     ProcessModel.query.filter_by(ProcessModel.process_id==componet.process_id).update({'process_status': 3})
        #     db.session.commit()

        db.session.commit()
        return Success.message, Success.code

