from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import ConfigParser
import sys, os
from flask_cors import CORS
cwd = os.path.join(os.getcwd(), sys.argv[0]) 
root_folder = (os.path.dirname(cwd))
os.environ["NLS_LANG"] = "GERMAN_GERMANY.UTF8" 
#Get the oracle database connection information
db_config = ConfigParser.SafeConfigParser()
db_config.read(os.path.join(root_folder,'config/connection.conf'))
db_dialect = db_config.get('db','dialect')
db_driver = db_config.get('db','driver')
db_hostname = db_config.get('db', 'host')
db_user = db_config.get('db', 'user')
db_password = db_config.get('db', 'password')
db_port = db_config.get('db', 'port')
db_database = db_config.get('db', 'database')
#SQLALCHEMY_DATABASE_URI = 'oracle://%s:%s@%s:%s/%s' % (db_user, db_password, db_hostname, db_port, db_sid)
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(db_dialect,db_driver,db_user,db_password,db_hostname,db_port,db_database)


print(SQLALCHEMY_DATABASE_URI)
print(db_hostname)

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Connect oracle://scott:tiger@127.0.0.1:1521/sidname
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_ECHO'] = True
app.config['root_folder'] = root_folder

# orm instance
db = SQLAlchemy(app)