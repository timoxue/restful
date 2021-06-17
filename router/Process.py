# encoding:UTF-8 

from threading import Condition
from flask_restful import Resource, Api, reqparse
from flask import Flask, jsonify, abort, request
from models import program
from models.Process import Process as ProcessModel
from models.Incident import Incident as IncidentModel
from models.Component import Component as ComponentModel
from models.program import Program as ProgramModel
from models.project import Project as ProjectModel
from models.db import db
from models.db import app
from flask_jwt import JWT, jwt_required, current_identity
from router.Message import MessageList
import json
import datetime
import decimal
from router.Status import Success, NotFound,NotUnique,DBError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import datetime
from sqlalchemy.sql import func

class ProcessList(Resource):
    @jwt_required()
    def get(self):
        username = current_identity.to_dict()['username']
        conditions = []
        parser = reqparse.RequestParser()
        parser.add_argument('role_type')
        args = parser.parse_args()
        role_type = args['role_type']

        if role_type == 'process_owner':
            conditions.append(ProcessModel.process_owner == username)
        if role_type == "experimenter":
            conditions.append(ProcessModel.experimenter == username)

        
        results = ProcessModel.query.filter(*conditions).filter(ProcessModel.process_status != 0).join(IncidentModel, IncidentModel.incident_id==ProcessModel.incident_id). \
        join(ProgramModel, ProgramModel.order_number==IncidentModel.order_number).\
        join(ProjectModel, ProjectModel.id==ProgramModel.pro_id).\
        with_entities(ProgramModel.pro_name, ProgramModel.pro_id,
                ProjectModel.finish_time,
                IncidentModel.incident_id, IncidentModel.create_name,IncidentModel.order_number, IncidentModel.experi_project, IncidentModel.experi_type,
                ProcessModel.process_id, ProcessModel.process_name, ProcessModel.start_time_d, ProcessModel.end_time_d, ProcessModel.process_name,ProcessModel.process_status, ProcessModel.experimenter).all()
        #incidents = [incident.to_dict() for incident in IncidentModel.query.filter_by(IncidentModel.process_status==args['process_status']).all()]
        #print(results)
        response_data = [dict(zip(result.keys(), result)) for result in results]
        for entity in response_data:
                entity['start_time_d'] = datetime.datetime.strftime(entity['start_time_d'], '%Y-%m-%d %H:%M:%S')
                entity['end_time_d'] = datetime.datetime.strftime(entity['end_time_d'], '%Y-%m-%d %H:%M:%S')
  
        return {'data':response_data}

class ProcessStatus(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('process_id', type=int)
        args = parser.parse_args()
        print(args)
        process_id = args['process_id']
        result = ProcessModel.query.filter(ProcessModel.process_id==process_id).with_entities(ProcessModel.process_id,ProcessModel.process_status).first()
        #print (result)
        response_data = dict(zip(result.keys(), result)) 
        return response_data
        

    def put(self):
        req_data = request.json
        value = {}
        process_id = req_data['process_id']
        value['process_status'] = req_data['process_status']
        if req_data.has_key('experimenter'):


            value['experimenter'] = req_data['experimenter']
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

        current_process = ProcessModel.query.filter(ProcessModel.process_id==process_id).first()
        last_procee_id = current_process.pre_process_id
        incident_id = current_process.incident_id
        if not last_procee_id: #如果没有前一步
            #改变incident的status 0=>1
            IncidentModel.query.filter(IncidentModel.incident_id==incident_id).update({'incident_status': 1})

        #db.session.commit()
        try:
            db.session.commit()
        except IntegrityError as e:
            print(e)
            return NotUnique.message, NotUnique.code
        except SQLAlchemyError as e: 
            print(e)
            return DBError.message, DBError.code
        return Success.message, Success.code


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)

class CheckProcessStatus(Resource):
    def post(self):
        req_data = request.json
        process_id = req_data['process_id']
        current_process = ProcessModel.query.filter(ProcessModel.process_id==process_id).first()
        next_process_id = current_process.pos_process_id
        incident_id = current_process.incident_id
        if next_process_id: #如果有下一步
            ProcessModel.query.filter(ProcessModel.process_id==process_id).update({'process_status': 4}) 
            ProcessModel.query.filter(ProcessModel.process_id==next_process_id).update({'process_status': 1})
            
            ComponentModel.query.filter(ComponentModel.process_id==process_id).update({ 'process_id': next_process_id,'experimenter':" "})
            ComponentModel.query.filter(ComponentModel.process_id==next_process_id).filter(ComponentModel.component_status1 == 3).update({'component_status1':1})

            #new message
            next_process = ProcessModel.query.filter(ProcessModel.process_id==next_process_id).first()
            MessageList().newMeassge(4,next_process.experiment_owner,next_process.process_owner)

        else:
            ProcessModel.query.filter(ProcessModel.process_id==process_id).update({'process_status': 4}) 
            IncidentModel.query.filter(IncidentModel.incident_id==incident_id).update({'incident_status': 2})
            #ComponentModel.query.filter(ComponentModel.process_id==process_id).filter(ComponentModel.component_status1 == 3).update({'component_status1':3})
        #db.session.commit()
        try:
            db.session.commit()
        except IntegrityError as e:
            print(e)
            return NotUnique.message, NotUnique.code
        except SQLAlchemyError as e: 
            print(e)
            return DBError.message, DBError.code
        return Success.message, Success.code

@app.route('/getOverviewProStatus')
@jwt_required()
def overviewStatus():
    username = current_identity.to_dict()['username']
    req_data = request.json
    conditions = []
    parser = reqparse.RequestParser()    
    parser.add_argument('role_type')
    args = parser.parse_args()
    role_type = args['role_type']
    if role_type == 'process_owner':
        conditions.append(ProcessModel.process_owner == username)
    if role_type == "experimenter":
        conditions.append(ProcessModel.experimenter == username)
    print(username)
    print (role_type)
    allIncident = ProcessModel.query.filter(*conditions).count() #分配给自己的工序
    finishIncident = ProcessModel.query.filter(*conditions).filter(ProcessModel.process_status == 4).count() #已完成
    assginIncident = ProcessModel.query.filter(*conditions).filter(ProcessModel.process_status == 2).count() #已分配和待领取
    processIncident = ProcessModel.query.filter(*conditions).filter(ProcessModel.process_status == 3).count() #实验中
    unassginIncident =  ProcessModel.query.filter(*conditions).filter(ProcessModel.process_status == 1).count()#待分配
    data = {
        "allIncident":allIncident,
        "finishIncident":finishIncident,
        "assginIncident":assginIncident,
        "processIncident":processIncident,
        "unassginIncident":unassginIncident

    }
    return data
def get_count(q):
    return q.with_entities(func.count()).scalar()
@app.route('/getDashBoardProcess/<order_number>')

def dashBoardProcess(order_number):
    conditions = []
    if order_number == 'All':

        conditions = []
    else:
        conditions.append(ComponentModel.order_number == order_number)
    inStore = get_count(ComponentModel.query.join(ProcessModel,ComponentModel.process_id == ProcessModel.process_id).filter(ComponentModel.component_status == 1)) #已入库
    inMeasure = get_count(ComponentModel.query.join(ProcessModel,ComponentModel.process_id == ProcessModel.process_id).filter(ProcessModel.process_name.like("%" +"测量"+ "%")))
    print(inMeasure)
    #results = [dict(zip(result.keys(), result)) for result in inMeasure]
    #print(results)
    inPaste = get_count(ComponentModel.query.join(ProcessModel,ComponentModel.process_id == ProcessModel.process_id).filter(ProcessModel.process_name.like("%" +"应变计粘贴"+ "%")))
    inLossless = get_count(ComponentModel.query.join(ProcessModel,ComponentModel.process_id == ProcessModel.process_id).filter(ProcessModel.process_name.like("%" +"无损"+ "%")))
    inConditions = get_count(ComponentModel.query.join(ProcessModel,ComponentModel.process_id == ProcessModel.process_id).filter(ProcessModel.process_name.like("%" +"环境调节"+ "%")))
    inExp = ComponentModel.query.filter(ComponentModel.component_status == 2).count()
    allIncident = ProcessModel.query.count() #分配给自己的工序
    finishIncident = ProcessModel.query.filter(ProcessModel.process_status == 4).count() #已完成
    assginIncident = ProcessModel.query.filter(ProcessModel.process_status == 2).count() #已分配且待领取
    processIncident = ProcessModel.query.filter(ProcessModel.process_status == 3).count() #实验中
    unassginIncident =  ProcessModel.query.filter(ProcessModel.process_status == 1).count()#待分配
    data = {
        "inStore":inStore,
        "inMeasure":inMeasure,
         "inPaste":inPaste,
         "inLossless":inLossless,
         "inConditions":inConditions,
         "inExp":inExp
    }
    return data

@app.route('/processAlert')
def processAlert():
    data = db.session.execute('SELECT * FROM sfincident.PROCESS_ALERT').fetchall()
    results = [dict(zip(result.keys(), result)) for result in data]
    for entity in results:
        entity['start_time_d'] = datetime.datetime.strftime(entity['start_time_d'], '%Y%m%d')
        entity['end_time_d'] = datetime.datetime.strftime(entity['end_time_d'], '%Y%m%d')
    return {'data': results}