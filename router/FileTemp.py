from flask_restful import Resource, Api, reqparse
from flask import Flask, jsonify, abort, request, redirect, flash
from utils.file import FileHandler 
from models.FileModel import FileModel
from models.fileTemp import FileTempModel
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from models.db import db
from models.db import app
import os
from os.path import join, dirname, realpath
import datetime
from router.Status import Success, NotFound, NotUnique,DBError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import send_file, send_from_directory, safe_join, abort
from flask_jwt import JWT, jwt_required, current_identity

class FileTemp(Resource):
    def post(self,f_key):
        fileTemp = FileTempModel()
        fileTemp = fileTemp.from_dict(request.json)
        db.session.add(fileTemp)
        #db.session.commit()
        try:
            db.session.commit()
        except IntegrityError as e:
            print(e)
            return NotUnique.message, NotUnique.code
        except SQLAlchemyError as e: 
            print(e)
            return DBError.message, DBError.code
        return Success.message, Success.code
    def get(self,f_key):
        fileTemp = FileTempModel.query.filter_by(f_key=f_key).order_by(FileTempModel.create_at.desc()).first()
        print (fileTemp)
        if fileTemp is None:
            return {'f_key':None,'f_id':None}, Success.code
        data = fileTemp.to_dict()
        return data