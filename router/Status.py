# -*- coding: utf-8 -*-
class Success:
    code = 200
    message = {'message': '提交成功'}

class NotUnique:
    code = 500
    message = {'message': '后台错误'}

class NotFound:
    code = 404
    message = {'message': '试验件编码不存在'}

class NotAllow:
    code = 406
    message = {'message': '不允许提交'}