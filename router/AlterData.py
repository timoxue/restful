from flask_restful import Resource
from flask import Flask, jsonify, abort, request

from models import Combined
from models.db import app
import datetime
from models.db import db
from models.alertData import AlterData as AlterDataModel
from router.Status import Success, NotFound,NotUnique,DBError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt import JWT, jwt_required, current_identity

class AlterDataList(Resource):
    def get(self):
        results = AlterDataModel.query.with_entities(AlterDataModel.create_at,AlterDataModel.des).all()

        response_data =  [dict(zip(result.keys(), result)) for result in results]

        for entity in response_data:
                entity['create_at'] = datetime.datetime.strftime(entity['create_at'], '%Y-%m-%d %H:%M:%S')
                
        return response_data
    


    def post(self):
        #print(json.load(request.json))
        alterData = AlterDataModel()
        alterData = alterData.from_dict(request.json)
        try:
            db.session.add(alterData)
            db.session.commit()
        except IntegrityError as e:
            print(e)
            return NotUnique.message, NotUnique.code
        except SQLAlchemyError as e: 
            print(e)
            return DBError.message, DBError.code
        return Success.message, Success.code    


