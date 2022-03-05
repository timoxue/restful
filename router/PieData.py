from flask_restful import Resource
from flask import Flask, jsonify, abort, request

from models import Combined
from models.db import app

from models.db import db
from models.pieData import PieData as PieDataModel
from router.Status import Success, NotFound,NotUnique,DBError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt import JWT, jwt_required, current_identity

class PieDataList(Resource):
    def get(self):
        results = PieDataModel.query.with_entities(PieDataModel.id,PieDataModel.data_type,PieDataModel.count).all()
        response_data =  [dict(zip(result.keys(), result)) for result in results]
        return response_data
    
    def put(self):
        request_data = request.json
        pieDataList = request_data['data']
        for value in pieDataList:
            #print (value)

            PieDataModel.query.filter(
                PieDataModel.id == value['id']).update(value)

            db.session.commit()
        return Success.message, Success.code        

