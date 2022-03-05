# -*- coding: utf-8 -*-
import re
from flask.wrappers import Response
from sqlalchemy.orm import compile_mappers
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import Constraint
from models import instore
from models import program
from models import Component_his
from models.instore import Instore
from flask_restful import Resource, Api, reqparse
from flask import Flask, jsonify, abort, request
from models.Incident import Incident as IncidentModel
from models.Component import Component as ComponentModel
from models.Component_his import ComponentHis as ComponentHisModel
from models.program import Program as ProgramModel
from models.project import Project as ProjectModel
from models.Process import Process as ProcessModel
from router.InStore import Instore as Instore
from models.db import app
from sqlalchemy import or_  
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt import JWT, jwt_required, current_identity
from flask import send_file, send_from_directory, safe_join, abort
from io import BytesIO
import os
import zipfile
from models.db import db
from router.Status import Success, NotFound,NotAllow, NotUnique,DBError
import datetime
from router.User import UserAuth
from models.FileModel import FileModel
class Component(Resource):
    def post(self):
        try:
            db.session.execute(
                ComponentModel.__table__.insert(),
                request.json['data']
            )
        #db.session.commit()
      
        except IntegrityError as e:
            print(e)
            return NotUnique.message, NotUnique.code
        except SQLAlchemyError as e: 
             print(e)
             return DBError.message, DBError.code
        db.session.commit()
        return Success.message, Success.code

    def put(self,component_unique_id):
        data = request.json['data']
       
        try:
            ComponentModel.query.filter_by(component_unique_id=component_unique_id).update(data)
        

            db.session.commit()
        except IntegrityError as e:
            print(e)
            return NotUnique.message, NotUnique.code
        except SQLAlchemyError as e: 
            print(e)
            return DBError.message, DBError.code
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
 
    for value in ComponentList:
        component = ComponentModel.query.filter(
            ComponentModel.component_unique_id == value['component_unique_id']).first()
        if component is None:
            return NotFound.message,NotFound.code

        elif component.component_status1 != status:  # 错误的入库类型
            
        
            uncomponentList.append(component.to_dict())

    if len(uncomponentList) == 0:
        return Success.message,Success.code
    else:
        return {'data':uncomponentList}
 
@app.route("/comOverview",methods=['GET'])
def comOverview():
    componentCount = db.session.query(ComponentModel).count()
    componentInstore = db.session.query(ComponentModel).filter(ComponentModel.component_status != None).filter(ComponentModel.component_status1 == None).count() #样品入库
    componentProcess = db.session.query(ComponentModel).filter(or_(ComponentModel.component_status1 != 5,ComponentModel.component_status1 != 6)).filter(ComponentModel.component_status == 2).count() #实验中
    componentDelivered = db.session.query(ComponentModel).filter(ComponentModel.component_status1 == 6).filter(ComponentModel.component_status == 1).count() #待交付
    
    # incidents = db.session.query(IncidentModel).count()
    # incidentsFinish = db.session.query(IncidentModel).filter(IncidentModel.incident_status == 2).count()
    # programAll = db.session.query(ProgramModel).count()
    # data = db.session.execute(
    #         'SELECT count(*) as count FROM PROGRAM_VIEW WHERE sample_num = is_finish'
    #     ).fetchall()

    # results = [dict(zip(result.keys(), result)) for result in data]
    # print(results)
    return {
        'componentCount':componentCount,
        'componentInstore':componentInstore,
        'componentProcess':componentProcess,
        'componentDelivered':componentDelivered
        
    }

@app.route("/checkComponent",methods=['POST'])
def checkComponent():
    request_data = request.json
    component_unique_id = request_data['component_unique_id']
    print(component_unique_id)
    is_type = request_data['is_type']
    conditions = []
    if 'id' in request_data:
        instore_id = request_data['id']
        conditions.append(ComponentModel.instore_id == instore_id)
    if 'out_id' in request_data:
        outstore_id = request_data['out_id']
        conditions.append(ComponentModel.outstore_id == outstore_id)
    if 'order_number' in request_data:
        order_number = request_data['order_number']
        conditions.append(ComponentModel.order_number == order_number)
    if 'conidtion' in request_data:
        in_condition = request_data['conidtion'] #标记出库还是入库  0：出库 1：入库
        if in_condition == 0:
            conditions.append(ComponentModel.component_status != 2 )
        else:
            conditions.append(ComponentModel.component_status == 2 )

    u = db.session.query(ComponentModel).filter(ComponentModel.component_unique_id == component_unique_id).first()
    if u is None:
        resp = jsonify({'message':'试验件编码不存在，请重新扫码'})
        # resp = Response({
        #      'message':'试验件编码不存在，请重新扫码'
        # })
        abort(404)
    else:
        u = db.session.query(ComponentModel).filter(*conditions).filter(ComponentModel.component_unique_id == component_unique_id).first()
        
        if u is None:
            resp = jsonify({'message':"试验件编码在当前委托单编号号不存在或已完成出入库！"})
            abort(404)
         

        if is_type == 0:  # 待测样品
            status = None
            status1 = 1

        elif is_type == 1:  # 1已完成样品
            status = 3 
            status1 = 6 #成品或者完成样品

        elif is_type == 2:  # 问题样品
            status = 5
            status1 = 5 #成品或者完成样品


        if u.component_status1 != status and u.component_status1 != status1:
            # 错误的入库类型
            resp = jsonify({'message':'试验件不符合入库或出库标准，请检查！'})
            # resp = Response({
            #     'message':'试验件入符合入库标准，请检查！'
            # })
            abort(500)
        else:
            if is_type != 0:
                i = db.session.query(IncidentModel).filter(IncidentModel.incident_id == u.incident_id).first()
                if i.incident_status != 2: #工单未审核
                    resp = jsonify({'message':'该工单未审核，试验件不可提交'})
                    abort(500)
                else:
                    return {'message': '试验件符合入库或出库标准'},Success.code
            else:
                return {'message': '试验件符合入库或出库标准'},Success.code
            
            # if u.component_status1 != status and u.component_status1 != status1:
            #   # 错误的入库类型
            #     resp = jsonify({'message':'试验件不符合入库或出库标准，请检查！'})
            # # resp = Response({
            # #     'message':'试验件入符合入库标准，请检查！'
            # # })
            #     abort(500)
            # else:
                    
          


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

@app.route('/incidentUncheckComponents/<incident_id>')
def incidentUncheckComponents(incident_id):
    u = db.session.query(ComponentModel).\
    filter(ComponentModel.incident_id == incident_id)\
    .all()
    result = [data.to_dict() for data in u]
    return {'data': result}


@app.route('/incidentComponents/<incident_id>')
def incidentComponents(incident_id):
    u = db.session.query(ComponentModel).filter(ComponentModel.incident_id == incident_id).all()
    result = [data.to_dict() for data in u]
    return {'data': result}


class ComponentList(Resource):
    @jwt_required()
    def get(self):
        username = current_identity.to_dict()['username']
        u_auth = UserAuth().getUserAuth(username)
        parser = reqparse.RequestParser()
        parser.add_argument('process_id', type=int)
        parser.add_argument('process_status', type=int)
        parser.add_argument('role_type')
        args = parser.parse_args()
        print(args)
        response_data = {}
        conditions = []
        role_type = args['role_type']
        if role_type == 'process_owner' and u_auth != 'adminAll':
            conditions.append(ComponentModel.process_owner == username)
        if role_type == "experimenter":
            conditions.append(ComponentModel.experimenter == username)        
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
        if response_data['process_status'] == 4: #当前工序已经完成，读历史components
            conditions = []
            if role_type == 'process_owner' and u_auth != 'adminAll':
                conditions.append(ComponentHisModel.process_owner == username)
            if role_type == "experimenter":
                conditions.append(ComponentHisModel.experimenter == username)          
            group_components = ComponentHisModel.query.filter(*conditions).filter(ComponentHisModel.incident_id == group_incident_id) \
            .filter(ComponentHisModel.process_id == args['process_id']).all()
        else:
            group_components = ComponentModel.query.filter(*conditions).filter(ComponentModel.incident_id == group_incident_id) \
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

    def post(self):
        try:
            db.session.execute(
                ComponentModel.__table__.insert(),
                request.json['data']
            )
        #db.session.commit()
      
        except IntegrityError as e:
            print(e)
            return NotUnique.message, NotUnique.code
        except SQLAlchemyError as e: 
             print(e)
             return DBError.message, DBError.code
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
    def put(self, component_unique_id):
        data = request.json['data']
        ComponentModel.query.filter(
            ComponentModel.component_unique_id == component_unique_id).update(data)
        try:
            db.session.commit()
        except IntegrityError as e:
            print(e)
            return NotUnique.message, NotUnique.code
        except SQLAlchemyError as e: 
            print(e)
            return DBError.message, DBError.code
        return Success.message, Success.code

@app.route("/ComponentHisStatus/<component_unique_id>",methods=['POST'])
def ComponentHisStatus(component_unique_id):
    value = request.json
    #status = value['component_status1']
    try:
        ComponentHisModel.query.filter_by(component_unique_id=component_unique_id).update(value)
        
 
        db.session.commit()
    except IntegrityError as e:
        print(e)
        return NotUnique.message, NotUnique.code
    except SQLAlchemyError as e: 
        print(e)
        return DBError.message, DBError.code
    return Success.message, Success.code    
    

 

@app.route("/checkComponentFailure",methods=['POST'])
def checkComponentFailure():
    incident_id = request.json['incident_id']
    type = request.json['type']
    if type == 'count':
        return {'data':  ComponentModel.query.filter_by(incident_id=incident_id).filter_by(is_check = 2).filter_by(component_status1=5).count()}
    else:

        return {'data': [component.to_dict() for component in ComponentModel.query.filter_by(incident_id=incident_id).filter_by(is_check = 2).filter_by(component_status1=5).all()]}


@app.route("/componentTime",methods=['GET'])
def componentTime():

    data = db.session.execute(
            'SELECT *  FROM component_series where finish != 0 limit 7'
        ).fetchall()

    results = [dict(zip(result.keys(), result)) for result in data]
    
    return {
        'data':results
    }


@app.route('/componentDetail/<component_unique_id>')
def componentDetail(component_unique_id):
    component = ComponentModel.query.filter(ComponentModel.component_unique_id == component_unique_id).join(ProcessModel,ProcessModel.process_id == ComponentModel.process_id).join(IncidentModel,IncidentModel.incident_id == ComponentModel.incident_id)\
        .join(ProgramModel, ProgramModel.order_number == IncidentModel.order_number) \
        .join(ProjectModel, ProjectModel.id == ProgramModel.pro_id) \
        .with_entities(ComponentModel.component_unique_id,ProgramModel.pro_name,ProgramModel.task_name_book,
        ProgramModel.create_name,ProjectModel.create_name.label('pro_create_name'),
        ComponentModel.process_id,ComponentModel.component_status,ComponentModel.component_status1,
        ComponentModel.create_at,ComponentModel.experiment_owner,ComponentModel.incident_id,
        ComponentModel.experimenter,ComponentModel.process_owner,ComponentModel.order_number,
        ComponentModel.is_check,
        ComponentModel.instore_id,ProcessModel.start_time_d,ProcessModel.end_time_d,IncidentModel.create_name,IncidentModel.experi_project,IncidentModel.experi_rely,IncidentModel.experi_type)\
        .first()
    print(component)
    process_id = component.process_id
    dis_process = ProcessModel.query.filter(ProcessModel.process_id == process_id) \
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
            ProcessModel.incident_id == group_incident_id).join(ComponentHisModel,ComponentHisModel.process_id == ProcessModel.process_id).filter(ComponentHisModel.component_unique_id == component_unique_id).order_by(ProcessModel.step_number).\
            with_entities(ProcessModel.process_name,ProcessModel.process_id,ProcessModel.start_time_d,ProcessModel.end_time_d,ProcessModel.process_owner,ComponentHisModel.experimenter,ComponentHisModel.experiment_sheet_id,ComponentHisModel.create_at).all()
    co_workers = set()
    group_processes_names = []
    print (group_processes)
    group_processes = [dict(zip(result.keys(), result))
                         for result in group_processes]
    
    component = dict(zip(component.keys(), component))
    for g_p in group_processes:
        co_workers.add(g_p['process_owner'])
        processObj = {}
        processObj['process_name'] = g_p['process_name']
        processObj['process_id'] = g_p['process_id']
        processObj['process_owner'] = g_p['process_owner']
        processObj['experimenter'] = g_p['experimenter']
        processObj['experiment_sheet_id'] = g_p['experiment_sheet_id']
        processObj['create_at'] = g_p['create_at']
        group_processes_names.append(processObj)
    #component = component.to_dict()
    component['planIncidentStartTime'] = group_processes[0]['start_time_d']
    component['planIncidentEndTime'] = group_processes[len(group_processes)-1]['end_time_d']
    component['co_experimenter'] = list(co_workers)
    component['processes'] = group_processes_names
    #response_data['component_unique_id'] = component.component_unique_id
    #response_data['component_status'] = component.component_status
    #response_data['component_status1'] = component.component_status1

    #print (component)

    return {'data':component}

@app.route('/componentId')
def componentId():
    result = ComponentModel.query.order_by(ComponentModel.update_at).first()
    componentId = result.component_unique_id
    return {
        "component_unique_id":componentId
    }
@app.route('/componentEfficiency')
def componentEfficiency():
    data = db.session.execute(
            'SELECT *  FROM efficiency limit 10'
        ).fetchall()

    results = [dict(zip(result.keys(), result)) for result in data]
  
    return {
        'data':results
    }

@app.route('/dowComponents/<file_id>')
def dowComponents(file_id):
    id_list = file_id.split(",")
    #data = request.json['list']
    com_his = ComponentHisModel.query.filter(ComponentHisModel.component_unique_id.in_(id_list))
    #寻找当前试验件ID对应的file-id
    results = [d.to_dict() for d in com_his]
    for r in results:
        file_id = r['experiment_sheet_id']
        print(file_id)
        # if file_id is None:
        #     pass
        # else:
        #     target_file = FileModel.query.filter(FileModel.id==file_id).first()
        #     if target_file is None:
        #         pass
        #     else:
        #         location = target_file.f_location
        #         file_name = target_file.f_filename
        #         extension = file_name.rsplit('.', 1)[-1].lower()
        #         f_name = str(file_id)+"."+extension
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zf:
        for _file in results:
            file_id = _file['experiment_sheet_id']
            target_file = FileModel.query.filter(FileModel.id==file_id).first()
            if target_file is None:
                pass
            else:
                location = target_file.f_location
                file_name = target_file.f_filename
                extension = file_name.rsplit('.', 1)[-1].lower()
                f_name = str(file_id)+"."+extension
                print(f_name)
                with open(os.path.join(location, f_name), 'rb') as fp:
                    zf.writestr(file_name, fp.read())        
    
    
    memory_file.seek(0)
    #print(memory_file)
    #return send_from_directory(location, filename=f_name, as_attachment=True)
    return send_file(memory_file, attachment_filename='test.zip', as_attachment=True)