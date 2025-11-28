import bcrypt, json, re, os
from dotenv import load_dotenv
import jwt
import modules.db_manager as database
load_dotenv(dotenv_path='./.env')
jwt_secret = os.getenv('JWT_SECRET')

def hash_passwd(create_user):
    def wrapper(*args):
        name = args[0]
        if not check_email(name):
            raise ValueError('Email Format not Accepted')
        passwd = args[1]
        acesso = args[2]
        salt = bcrypt.gensalt()
        hashed_passwd = bcrypt.hashpw(passwd.encode(), salt)
        try:
            create_user(name, hashed_passwd, acesso)
        except ValueError:
            raise ValueError
        else:
            return True
    return wrapper

def check_hash(login_user):
    def wrapper(*args):
        username = args[0]
        password = args[1]
        hashed_password = database.get_password(username)
        if bcrypt.checkpw(password.encode(), hashed_password.encode()):
            if login_user(username, hashed_password):
                return True
            else:
                return False
        else:
            raise ValueError('Wrong Password')
    return wrapper

def check_email(email:str) -> bool:
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return False
    else:
        return True
     
def check_cookie(cookie, acess_req):
    token = jwt.decode(cookie['jwt_token'], jwt_secret, algorithms='HS256')
    if token['acesso'] == acess_req or token['acesso'] == 'sudo':
        return True
    else:
        return False
    
def check_id(func):
    def wrapper(*args):
        token = jwt.decode(args[0]['jwt_token'], jwt_secret, algorithms='HS256')
        user_id = func(token['name'])
        id_to_check = args[1]
        if int(user_id[0]) == (id_to_check):
            return True
        else:
            return False
    return wrapper