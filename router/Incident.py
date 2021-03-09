from flask_restful import Resource, Api, reqparse
from flask import Flask, jsonify, abort, request
from models.Process import Process as ProcessModel
from models.Incident import Incident as IncidentModel
from models.Component import Component as ComponentModel
from models.db import db
from router.Status import Success, NotFound


class Incident(Resource):
    def post(self):
        req_data = request.json()
        #1. get process list and component_list
        component_list = req_data['component_list']
        process_list = req_data['process_list']

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
            process_list[i].incident_id = incident.incident_id
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
        db.session.execute(
            ProcessModel.__table__.update(),
            [p.to_dict() for p in update_process_list]
        )
        db.session.commit()

        #6. update insert into Component table
        for i, component in enumerate(component_list):
            component[i].incident_id = incident.incident_id
        db.session.execute(
            ComponentModel.__table__.insert(),
            component_list
        )
        db.session.commit()