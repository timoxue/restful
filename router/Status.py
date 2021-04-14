# -*- coding: utf-8 -*-
class Success:
    code = 200
    message = {'message': 'Success'}

class NotUnique:
    code = 500
    message = {'message': '数据不唯一'}

class NotFound:
    code = 404
    message = {'message': 'Not Found'}