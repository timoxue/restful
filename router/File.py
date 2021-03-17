from flask_restful import Resource, Api, reqparse
from flask import Flask, jsonify, abort, request
from utils.file import FileHandler 
from models.FileModel import FileModel
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from models.db import db
from models.db import app
from os.path import join, dirname, realpath

from router.Status import Success, NotFound
from flask import send_file, send_from_directory, safe_join, abort

class File(Resource):
    def get(self):
        return send_from_directory("/upload/updated/gongdan", filename="test.doc", as_attachment=True)
    
    def post(self):
        saved_file = request.files.get('file')
        #filename = secure_filename(saved_file.filename)     
        #save file
        # "update" is updated file
        # 'gongda' is category, is predefined in config/upload.conf
        #print("file:", filename)
        file_location = FileHandler("update", "gongdan").upload(saved_file, "test.txt")
        '''
        file_json = {
            'f_filename': "test", 
            'file_location': file_location,
            'f_id': "12345",
            'f_owner': "system",
            'is_delete': 'false'
        }
        file = FileModel().from_dict(file_json)
        #print(user.u_email)
        db.session.add(file)
        db.session.commit()
        '''
        return Success.message, Success.code



@app.route("/getFile/<file_name>")
def get_image(file_name):
    tem_path = FileHandler("template", "instore").get_file()
    print (tem_path)
    try:
        return send_from_directory(tem_path, filename=file_name, as_attachment=True)
    except IOError:
        abort(404)       