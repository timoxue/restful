from flask_restful import Resource, Api, reqparse
from flask import Flask, jsonify, abort, request
from models.Component import ComponentModel
from models.db import db
from router.Status import Success, NotFound

class Component(Resource):
    def post(self):
        #print(json.load(request.json))
        parser = reqparse.RequestParser()
        #parser.add_argument('rate', type=int, help='Rate cannot be converted')
        parser.add_argument('data')
        args = parser.parse_args()
        #print(args['data'])
        db.session.execute(
            ComponentModel.__table__.insert(),
            args['data']
        )
        db.session.commit()
        return Success.message, Success.code