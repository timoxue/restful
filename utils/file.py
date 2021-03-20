from config import upload_config
import os
from config import root_folder
import datetime

class FileHandler(object):    
    def __init__(self, category):
        # file_type is "tempate or updated"
        # category should be pre-defined under config/upload.conf
        self.short_location = os.path.join(upload_config.get(category, "base_folder"), upload_config.get(category, "update_folder"))
        if category == 'template':
            self.file_location = os.path.join(root_folder, self.short_location)
        else:
            self.file_location = os.path.join(root_folder, self.short_location, datetime.datetime.now().strftime("%Y%m%d"))
        self.check_folder(self.file_location)
    
    def upload(self, data, filename):
    # file should be from request as request.data
        '''
        with open(os.path.join(self.file_location, filename), "wb") as fp:
            fp.write(data)
        '''
        data.save(os.path.join(self.file_location, filename))
        return self.short_location

    def get_file(self):
        return self.file_location
    
    def check_folder(self, location):
        if os.path.isdir(location):
            return True
        else:
            os.makedirs(location)
            return False
