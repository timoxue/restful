from werkzeug.security import safe_str_cmp
from models.user import User as UserModel
from models.db import db
from router.Status import PSError


def authenticate(username, password):
    print('authenticate')
    users_in_memory = UserModel.query.filter_by(is_delete = False).all()
   
    #username_table would give the id, username, password from the userid_mapping, so we do not have to iterate over the users again and again
    username_table = {u.username: u for u in users_in_memory}
    #userid_table is the userid mapping
   
    #None is the default value i.e if there is no username like the given.
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.u_password, password):

        print (user)
        return user
    # else:
    #     print ('error')
    #     return PSError.message, PSError.code


#Identity function takes in the payload (payload is the contents of the jwt token)
def identity(payload):
    #extract the user id from that payload
    userid = payload['identity']
    users_in_memory = UserModel.query.filter_by(is_delete = False).all()
    #print(users_in_memory)
    #username_table would give the id, username, password from the userid_mapping, so we do not have to iterate over the users again and again
   
    #userid_table is the userid mapping
    userid_table = {u.id: u for u in users_in_memory}
    #retrieve the user which matches this userid
    return userid_table.get(userid, None)