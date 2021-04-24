#### 安装依赖
aniso8601        9.0.1
certifi          2016.2.28
click            7.1.2
configparser     4.0.2
cx-Oracle        7.3.0
Flask            1.1.2
Flask-RESTful    0.3.8     c:\users\timot\.conda\envs\flask\lib\site-packages
Flask-SQLAlchemy 2.4.4
itsdangerous     1.1.0
Jinja2           2.11.3
MarkupSafe       1.1.1
pip              20.0.2
pytz             2021.1
setuptools       36.4.0
six              1.15.0
SQLAlchemy       1.3.23
Werkzeug         1.0.1
wheel            0.36.2
wincertstore     0.2

### 安装 flask_restful, flask, flask-sqlalchemy, cx-Oracle==7.3 pymysql

### git clone 

### 修改数据库链接文件, 在config.connection.conf

### 生成数据库表: python init.py build
### 插入数据: python init.py update
###  删除表: python init.py clean

## 所有Model相关的在models 目录下
## 所有router的业务逻辑在router目录下

## 修改url路径，如“localhost:5000/user/<user_id>”, 在start.py 文件里

##  启动server python start.py 

## 测试user get，"http://127.0.0.1:5000/user/admin"
