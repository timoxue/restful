# encoding:UTF-8 

from db import db

class User(db.Model):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, db.Sequence('id_seq'), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    u_id = db.Column(db.String(32),unique = True,nullable = False)
    u_password = db.Column(db.String(32),unique = True,nullable = False)
    u_authority = db.Column(db.String(256),unique = True,nullable = False)
    u_department = db.Column(db.String(32),unique = True,nullable = False)
    is_delete = db.Column(db.Boolean())
    u_email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    # def select_user(self):

    #     users_list = User.query.all()
    

    
    #查询用户名称为 fuyong 的第一个用户, 并返回用户实例, 
    #因为之前定义数据库的时候定义用户名称唯一, 所以数据库中用户名称为 test 的应该只有一个.
    #user = User.query.filter_by().first()
    #or
    #user = User.query.filter(User.username == 'fuyong').first()
 
    #模糊查询, 查找用户名以abc 结尾的所有用户
    #users_list = User.query.filter(User.username.endsWith('g')).all()
 
    #查询用户名不是 fuyong 的第一个用户
    #user = User.query.filter(User.username != 'fuyong').first()