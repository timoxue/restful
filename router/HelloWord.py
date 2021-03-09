from flask_restful import Resource, Api, reqparse

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
    
    def post(self):
        parser = reqparse.RequestParser()
        #parser.add_argument('rate', type=int, help='Rate cannot be converted')
        parser.add_argument('data')
        args = parser.parse_args()
        print(args['data'])