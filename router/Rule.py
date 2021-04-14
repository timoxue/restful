from flask_restful import Resource
from flask import Flask, jsonify, abort, request
from models.db import db
from models.RuleModel import RuleModel as RuleModel

from router.Status import Success, NotFound
from flask_jwt import JWT, jwt_required, current_identity
from models.db import app

class RuletList(Resource):
    def get(self):
        
        
        rules = [rule.to_dict() for rule in RuleModel.query.all()]
     
        return {'data':rules}
    
 