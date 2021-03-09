from flask_restful import Resource, Api, reqparse
from flask import Flask, jsonify, abort, request

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
    
    def post(self):
        print(request.json['data'])
        print("go!")
        #parser.add_argument('rate', type=int, help='Rate cannot be converted')
        