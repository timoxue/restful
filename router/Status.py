# -*- coding: utf-8 -*-
class Success:
    code = 200
    message = {'message': '提交成功'}

class NotUnique:
    code = 500
    message = {'message': '数据提交有问题，请检查'}

class NotFound:
    code = 404
    message = {'message': '未找到'}

class NotAllow:
    code = 406
    message = {'message': '不允许提交'}

class DBError:
    code = 500
    message = {'message': '数据库报错'}

class PSError:
    code = 500
    message = {'message': '用户名密码错误'}
