import ConfigParser
import os,sys

## read some config file
cwd = os.path.join(os.getcwd(), sys.argv[0]) 
root_folder = (os.path.dirname(cwd))
db_config = ConfigParser.SafeConfigParser()
db_config.read([os.path.join(root_folder,'config/upload.conf'),os.path.join(root_folder,'config/connection.conf')])
gloabl_config = db_config