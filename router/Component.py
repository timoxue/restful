from flask_restful import Resource, Api, reqparse
from flask import Flask, jsonify, abort, request
from models.Component import Component as ComponentModel
from models.db import db
from router.Status import Success, NotFound

class Component(Resource):
    def post(self):
        db.session.execute(
            ComponentModel.__table__.insert(),
            request.json['data']
        )
        db.session.commit()
        return Success.message, Success.code