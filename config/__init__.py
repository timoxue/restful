import ConfigParser
import os,sys

## read some config file
cwd = os.path.join(os.getcwd(), sys.argv[0]) 
root_folder = (os.path.dirname(cwd))
config = ConfigParser.SafeConfigParser()
config.read(os.path.join(root_folder,'config/upload.conf'))
upload_config = config

cwd = os.path.join(os.getcwd(), sys.argv[0]) 
root_folder = os.path.dirname(cwd)
