# -*- coding: utf-8 -*-
from warnings import resetwarnings
from models import instore
from models import program
from models.instore import Instore
from flask_restful import Resource, Api, reqparse
from flask import Flask, jsonify, abort, request
from models.Incident import Incident as IncidentModel
from models.Component import Component as ComponentModel
from models.program import Program as ProgramModel
from models.project import Project as ProjectModel
from models.Process import Process as ProcessModel
from router.InStore import Instore as Instore
from models.db import app

from models.db import db
from router.Status import Success, NotFound,NotAllow
import datetime


class Component(Resource):
    def post(self):
        db.session.execute(
            ComponentModel.__table__.insert(),
            request.json['data']
        )
        db.session.commit()
        return Success.message, Success.code


@app.route('/scanCode',methods=['POST'])
def scanCode():
    request_data = request.json
    ComponentList = request_data['data']
    instore_id = request_data['id']
    uncomponentList = []
    is_type = Instore().checkInstoreType(instore_id)
    # check instore type
    if is_type == 0:  # 待测样品
        status = None

    elif is_type == 1:  # 1已完成样品
        status = 3

    elif is_type == 2:  # 问题样品
        status = 5
    print(status)
    for value in ComponentList:
        component = ComponentModel.query.filter(
            ComponentModel.component_unique_id == value['component_unique_id']).first()
        print (component)
        if component is None:
            return NotFound.message,NotFound.code

        elif component.component_status1 != status:  # 错误的入库类型
            print (component.component_status1)
        
            uncomponentList.append(component.to_dict())

    if len(uncomponentList) == 0:
        return Success.message,Success.code
    else:
        return {'data':uncomponentList}
 
@app.route("/comOverview",methods=['GET'])
def comOverview():
    componentCount = db.session.query(ComponentModel).count()
    componentFinish = db.session.query(ComponentModel).filter(ComponentModel.component_status == 6).filter(ComponentModel.component_status == 1).count() #成品
    componentOut = db.session.query(ComponentModel).filter(ComponentModel.component_status == 6).filter(ComponentModel.component_status == 2).count() #交付
    incidents = db.session.query(IncidentModel).count()
    incidentsFinish = db.session.query(IncidentModel).filter(IncidentModel.incident_status == 2).count()
    programAll = db.session.query(ProgramModel).count()
    data = db.session.execute(
            'SELECT count(*) as count FROM sfincident.PROGRAM_VIEW WHERE sample_num = is_finish'
        ).fetchall()

    results = [dict(zip(result.keys(), result)) for result in data]
    print(results)
    return {
        'componentCount':componentCount,
        'componentFinish':componentFinish,
        'componentOut':componentOut,
        'incidents':incidents,
        'incidentsFinish':incidentsFinish,
        'programAll':programAll,
        'programFinish':results[0]['count']
    }



@app.route('/addExComponent/<order_number>')
def addExComponent(order_number):

    u = db.session.query(ComponentModel).filter(
        ComponentModel.order_number == order_number).filter(ComponentModel.component_status == 1).filter(ComponentModel.component_status1 == 0).all()
    #print ((u))
    result = [data.to_dict() for data in u]
    return {'data': result}


@app.route("/loadCodeComponent/<instore_id>")
def loadCodeComponent(instore_id):
    u = db.session.query(ComponentModel).filter(
        ComponentModel.instore_id == instore_id).filter(ComponentModel.component_status == 0).all()
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
        # 1. Get current process
        dis_process = ProcessModel.query.filter(ProcessModel.process_id == args['process_id']) \
            .join(IncidentModel, IncidentModel.incident_id == ProcessModel.incident_id) \
            .join(ProgramModel, ProgramModel.order_number == IncidentModel.order_number) \
            .join(ProjectModel, ProjectModel.id == ProgramModel.pro_id) \
            .with_entities(ProgramModel.pro_name, ProgramModel.pro_id, ProgramModel.order_number, ProgramModel.task_id, ProgramModel.program_id,
                           ProjectModel.finish_time,
                           IncidentModel.incident_id, IncidentModel.create_name, IncidentModel.experi_type,
                           ProcessModel.process_id, ProcessModel.process_name,
                           ProcessModel.start_time_d, ProcessModel.end_time_d,
                           ProcessModel.process_name, ProcessModel.process_status, ProcessModel.experimenter, ProcessModel.process_owner, ProcessModel.experiment_sheet_id).all()
        print(dis_process)
        response_data = [dict(zip(result.keys(), result))
                         for result in dis_process]

        for entity in response_data:
            entity['start_time_d'] = datetime.datetime.strftime(
                entity['start_time_d'], '%Y-%m-%d %H:%M:%S')
            entity['end_time_d'] = datetime.datetime.strftime(
                entity['end_time_d'], '%Y-%m-%d %H:%M:%S')
        response_data = response_data[0]
        # 2 Get group process under the same incident
        group_incident_id = response_data['incident_id']
        group_processes = ProcessModel.query.filter(
            ProcessModel.incident_id == group_incident_id).order_by(ProcessModel.step_number).all()
        co_workers = set()
        group_processes_names = []
        for g_p in group_processes:
            co_workers.add(g_p.process_owner)
            processObj = {}
            processObj['process_name'] = g_p.process_name
            processObj['process_id'] = g_p.process_id
            processObj['process_owner'] = g_p.process_owner
            group_processes_names.append(processObj)
        response_data["co_experimenter"] = list(co_workers)
        response_data["processes"] = group_processes_names

        # 3 get group Components
        group_components = ComponentModel.query.filter(ComponentModel.incident_id == group_incident_id) \
            .all()
        components_data = [result.to_dict() for result in group_components]

        for entity in components_data:
            del entity['create_at']
            del entity['update_at']
        #del components_data['create_at']
        #del components_data['update_at']
        # 4 update return data
        response_data['componentlist'] = components_data
        # response_data.update(components_data)

        return {'data': response_data}

    def put(self):
        request_data = request.json
        ComponentList = request_data['data']
        if 'id' in request_data:
            instore_id = request_data['id']
            print (instore_id)
        for value in ComponentList:
            print (value)
            if 'component_status1' not in value:
                is_type = Instore().checkInstoreType(instore_id)
                if is_type == 0:  # 待测样品
                    status = 0

                elif is_type == 1:  # 1已完成样品
                    status = 6

                elif is_type == 2:  # 问题样品
                    status = 5
                value['component_status1'] = status
            ComponentModel.query.filter(
                ComponentModel.component_unique_id == value['component_unique_id']).update(value)

            db.session.commit()
        return Success.message, Success.code


class CheckComponent(Resource):
    def post(self):
        request_data = request.json
        component_list = request_data['data']
        for i, _ in enumerate(component_list):
            value = {}
            componet_id = component_list[i]['component_unique_id']
            # value['']

        component_status1 = request_data['component_status1']
        component_status = request_data['component_status']
        component_id = request_data['id']
        #check_process = request_data['check_process']

        componet = ComponentModel.query.filter(
            ComponentModel.id == component_id).first()

        ComponentModel.query.filter_by(ComponentModel.id == component_id).update(
            {'component_status1': component_status1, "component_status": component_status})
        #total_num = ComponentModel.query.join(ProcessModel, ComponentModel.process_id==ProcessModel.process_id).count()
        #finished_num = ComponentModel.query.join(ProcessModel, ComponentModel.process_id==ProcessModel.process_id).filter(ComponentModel.component_status1==2).count()

        # if check_process and (total_num==finished_num):
        #     ProcessModel.query.filter_by(ProcessModel.process_id==componet.process_id).update({'process_status': 3})
        #     db.session.commit()

        db.session.commit()
        return Success.message, Success.code


class ReportFailureComponent(Resource):
    def post(self, component_unique_id):
        ComponentModel.query.filter(
            ComponentModel.component_unique_id == component_unique_id).update({'component_status1': 5})
        db.session.commit()
        return Success.message, Success.code




@app.route("/componentTime",methods=['GET'])
def componentTime():

    data = db.session.execute(
            'SELECT *  FROM sfincident.component_series'
        ).fetchall()

    results = [dict(zip(result.keys(), result)) for result in data]
    print(results)
    return {
        'data':results
    }
