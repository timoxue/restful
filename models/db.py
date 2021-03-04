from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import ConfigParser
import sys, os

cwd = os.path.join(os.getcwd(), sys.argv[0]) 
root_folder = (os.path.dirname(cwd))

#Get the oracle database connection information
db_config = ConfigParser.SafeConfigParser()
db_config.read(os.path.join(root_folder,'config/connection.conf'))
db_hostname = db_config.get('db', 'host')
db_user = db_config.get('db', 'user')
db_password = db_config.get('db', 'password')
db_port = db_config.get('db', 'port')
db_sid = db_config.get('db', 'sid')
SQLALCHEMY_DATABASE_URI = 'oracle://%s:%s@%s:%s/%s' % (db_user, db_password, db_hostname, db_port, db_sid)

print(SQLALCHEMY_DATABASE_URI)
print(db_hostname)

app = Flask(__name__)
# Connect oracle://scott:tiger@127.0.0.1:1521/sidname
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_ECHO'] = True
app.config['root_folder'] = root_folder

# orm instance
db = SQLAlchemy(app)