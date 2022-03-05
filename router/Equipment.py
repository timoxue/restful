from flask_restful import Resource
from flask import Flask, jsonify, abort, request
import json
from models import Combined
from models.db import app
import datetime
from models.db import db
from models.equipment import Equipment as EquipmentModel
from router.Status import Success, NotFound,NotUnique,DBError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt import JWT, jwt_required, current_identity

class Equipement(Resource):
    def post(self):       
        result = request.json['data']
        id = request.json['id']
        #db.session.execute("truncate table equipment")
        
        for i in result:
            Equipment = EquipmentModel()
            #equip = Equipment.from_dict(i)
            EquipmentModel.query.filter_by(id=id).update(i)
            
            db.session.commit()
           
        return Success.message, Success.code
    
    def put (self,id):
        data = request.json['data']
       
        try:
            EquipmentModel.query.filter_by(id=id).update(data)
            

            db.session.commit()
        except IntegrityError as e:
            print(e)
            return NotUnique.message, NotUnique.code
        except SQLAlchemyError as e: 
            print(e)
            return DBError.message, DBError.code
        return Success.message, Success.code 

class EquipementList(Resource):
    def get(self):
        results = EquipmentModel.query.all()
        response_data =  [result.to_dict() for result in results]
        return response_data

    # def post(self):
    #     #print(json.load(request.json))
    #     data = json.loads(request.get_data(as_text=True))
    #     print(data.data)
    #     equipment = EquipmentModel()
    #     equipment = equipment.from_dict(data.data)
    #     try:
    #         db.session.add(equipment)
    #         db.session.commit()
    #     except IntegrityError as e:
    #         print(e)
    #         return NotUnique.message, NotUnique.code
    #     except SQLAlchemyError as e: 
    #         print(e)
    #         return DBError.message, DBError.code
    #     return Success.message, Success.code


 


