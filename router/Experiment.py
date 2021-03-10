# - *- coding: utf- 8 - *-
from flask_restful import Resource, Api, reqparse
from flask import Flask, jsonify, abort, request
from models.Experiment import Experiment as ExperimentModel
from models.db import db
from router.Status import Success, NotFound

class Experiment(Resource):
    def post(self):
        experi = ExperimentModel()
        experi = experi.from_dict(request.json)
        db.session.add(experi)
        db.session.commit()
        return Success.message, Success.code
    
    def get(self):
        # experi0 = ExperimentModel(experiment_name="测量工序", experi_step =0, experi_type ="CAI")
        # experi1 = ExperimentModel(experiment_name='无损工序', experi_step =1, experi_type ="CAI")
        # experi2 = ExperimentModel(experiment_name='冲击工序', experi_step =2, experi_type ="CAI")
        # experi3 = ExperimentModel(experiment_name='无损工序', experi_step =3, experi_type ="CAI")
        # experi4 = ExperimentModel(experiment_name='应变剂黏贴工序', experi_step =4, experi_type ="CAI")
        # experi5 = ExperimentModel(experiment_name='压缩工序', experi_step =5, experi_type ="CAI")
        # db.session.add(experi0)
        # db.session.add(experi1)
        # db.session.add(experi2)
        # db.session.add(experi3)
        # db.session.add(experi4)
        # db.session.add(experi5)
        # db.session.commit()
        response_data = {}
        experiments = ExperimentModel.query.order_by(ExperimentModel.experi_type, ExperimentModel.experi_step).all()
        for ex in experiments:
            if ex.experi_type not in response_data.keys():
                response_data[ex.experi_type] = []
            response_data[ex.experi_type].append(ex.experiment_name)
        return response_data, Success.code