import bcrypt, json, re, os
from dotenv import load_dotenv
import jwt
import modules.db_manager as database
load_dotenv(dotenv_path='./.env')
jwt_secret = os.getenv('JWT_SECRET')

def hash_passwd(func):
    def wrapper(*args):
        name = args[0]
        passwd = args[1]
        acesso = args[2]
        salt = bcrypt.gensalt()
        hashed_passwd = bcrypt.hashpw(passwd.encode(), salt)
        try:
            func(name, hashed_passwd, acesso)
        except ValueError:
            raise ValueError
        else:
            return True
    return wrapper

def check_hash(passwd:str, hashed_passwd:str) -> bool:
    return bcrypt.checkpw(passwd.encode(), hashed_passwd.encode())

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
    
def check_identity(cookie, id):
    token = jwt.decode(cookie['jwt_token'], jwt_secret, algorithms='HS256')
    return f'{database.check_identity(token['name'])}'