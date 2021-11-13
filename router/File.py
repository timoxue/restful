from flask_restful import Resource, Api, reqparse
from flask import Flask, jsonify, abort, request, redirect, flash
from utils.file import FileHandler 
from models.FileModel import FileModel
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from models.db import db
from models.db import app
import os
from os.path import join, dirname, realpath
import datetime
from router.Status import Success, NotFound, NotUnique,DBError
from flask import send_file, send_from_directory, safe_join, abort
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

#import logging

ALLOWED_EXTENSIONS = ['doc', 'docx', 'xlsx', 'txt', 'ppt', 'pptx','png','pdf']

class File(Resource):

    
    #@jwt_required()
    def post(self):
        category = request.form['category']
        #username = current_identity.to_dict()['username']
        username="tim"
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            filename = file.filename
            handler =  FileHandler(category)
            #print(file_path)
            file_json = {
                'f_filename': filename, 
                'f_location': handler.file_location,
                'f_category': category,
                'f_owner': username,
                'is_delete': False
            }
            print (file_json)
            file_to_save = FileModel().from_dict(file_json)
            try:
                db.session.add(file_to_save)
            #db.session.commit()
                db.session.commit()
            except IntegrityError as e:
                print(e)
                return NotUnique.message, NotUnique.code
            except SQLAlchemyError as e: 
                print(e)
                return DBError.message, DBError.code
            #logging.info("successfully insert a file record: " +  [k +": "+ v for (k,v) in  dict.items()])
            handler.upload(file, str(file_to_save.id) + "." + filename.rsplit('.', 1)[-1].lower())
            #logging.info("successfully save a file as: " +  str(file_to_save.id) + "." + filename.rsplit('.', 1)[1].lower())
        return {'file_id': file_to_save.id}, Success.code

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/getFile/<file_id>")
def get_file(file_id):
    target_file = FileModel.query.filter(FileModel.id==file_id).first()
    if target_file is None:
        return {'message': 'File Not Found'}, Success.code
    #category = target_file.f_category
    location = target_file.f_location
    file_name = target_file.f_filename
    extension = file_name.rsplit('.', 1)[-1].lower()
    f_name = str(file_id)+"."+extension
    #tem_path = os.path.join(location, str(file_id)+"." + extension)

    try:
        return send_from_directory(location, filename=f_name, as_attachment=True)
    except IOError:
        abort(404)       