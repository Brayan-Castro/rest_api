from flask import Flask, Response, make_response, jsonify
from flask import request
import modules.db_manager as database
import modules.status as status_code
import jwt
from dotenv import load_dotenv
import os
import datetime
app = Flask(__name__)
jwt_secret = os.getenv('JWT_SECRET')
"""
Acess Level
    sudo:
        acess to everything;
        can update, add or remove admin status;
        can update, add or remove users;
    admin:
        acess to everything;
        cannot update, add or remove admin status;
        can update, add or remove users;
    user:
        curated acess;
        cannot update, add or remove admin status;
        can update, remove or add itself;
"""

"""
Endpoints
    /api/users
    /api/users/<id>
    /auth/login
    /auth/register
"""

def main():
    @app.route("/api/users", methods=['GET', 'DELETE']) #type: ignore
    def return_users():
        """
        How to use?
            Simply acess the endpoint (/api/users) with the desired HTTP Method, currently supports these methods:
                [GET]
                    Returns a JSON with the user data regarding all the users in this database, if the database is empty, it raises an HTTP Response with the code 204.
                [POST]
                    Tries to create a user on the database, requires and additional payload consisting of a JSON file containing a dict with the keys 'name' and 'passwd' with the content-type of 'application/json',
                    on sucess, returns an HTTP Response with the code 201, on failure, returns an HTTP Response with the code 500.
                    request example: session.post("http://127.0.0.1:5000/api/users", headers = {'Content-Type': 'application/json'}, data=json.dumps({'name': 'teste', 'passwd': 'teste', 'acesso': 'admin'}))
                [DELETE]
                    Tries to remove a user from the database, requires and additional payload consisting of a JSON file containing a dict with the keys 'name' and 'passwd' with the content-type of 'application/json',
                    on sucess, returns an HTTP Response with the code 200, on failure, returns an HTTP Response with the code 204.
                    request example: session.delete("http://127.0.0.1:5000/api/users", headers = {'Content-Type': 'application/json'}, data=json.dumps({'name': 'teste', 'passwd': 'teste'}))
        """
        try:
            data = request.json
        except:
            ...
        else:
            name = data['name'] #type: ignore
            passwd = data['passwd'] #type: ignore
            # acesso = data['acesso'] #type: ignore

        if request.method == 'GET':
            try:
                name #type: ignore
            except NameError:
                if check_cookie(request.cookies, 'admin'):
                    try:
                        return jsonify(database.see_user())
                    except ValueError:
                        return Response('Database is Empty', status=status_code.NO_CONTENT)
                else:
                    return Response('Unauthorized Acess', status=status_code.UNAUTHORIZED)
            else:
                try:
                    return jsonify(database.see_user(name=name, passwd=passwd)) #type: ignore
                except ValueError:
                    return Response('Database is Empty', status=status_code.NO_CONTENT)  
        elif request.method == 'DELETE':
            if check_cookie(request.cookies, 'admin'):
                try:
                    database.remove_user(name, passwd) #type: ignore
                    return Response('User was deleted', status=status_code.OK)
                except ValueError:
                    return Response('User not found', status=status_code.NO_CONTENT)
            else:
                return Response('Unauthorized Acess', status=status_code.UNAUTHORIZED)
        else:
            return Response('Method not Allowed', status=status_code.METHOD_NOT_ALLOWED)
        
    @app.route('/api/users/<int:id>', methods=['GET', 'DELETE']) #type: ignore
    def return_user_with_id(id):
        if check_cookie(request.cookies, 'admin'):
            if request.method == 'GET':
                try:
                    return jsonify(database.see_user(id=id))
                except ValueError:
                    return Response('User not found', status=status_code.NO_CONTENT)
            elif request.method == 'DELETE':
                try:
                    database.remove_user(id) #type: ignore
                    return Response('User was deleted', status=status_code.OK)
                except ValueError:
                    return Response('User not found', status=status_code.NO_CONTENT)
        else:
            return Response('Unauthorized Acess', status=status_code.UNAUTHORIZED)
            
    @app.route('/auth/login')
    def login():
        data = request.json
        name = data['name'] #type: ignore
        passwd = data['passwd'] #type: ignore
        acesso = data['acesso'] #type: ignore

        try:
            database.see_user(name=name, passwd=passwd)
        except ValueError:
            return Response('User not found', status=status_code.NO_CONTENT)
        else:
            response = make_response(jsonify({'login_status': 'Successful'}))
            jwt_token = jwt.encode({'name': name, 'acesso': acesso}, jwt_secret, algorithm='HS256')
            response.set_cookie('jwt_token', value=jwt_token)
            return response
        
    @app.route('/auth/register', methods=['POST'])
    def register():
        data = request.json
        name = data['name'] #type: ignore
        passwd = data['passwd'] #type: ignore
        acesso = data['acesso'] #type: ignore

        if request.method == 'POST':
            if acesso == 'sudo':
                if database.check_sudo():
                    try:
                        database.create_user(name, passwd, 'sudo')
                    except ValueError:
                        return Response('Unable to create sudo', status=status_code.INTERNAL_SERVER_ERROR)
                    else:
                        return Response('Sudo was created', status=status_code.CREATED)
                else:
                    return Response('Sudo already exists', status=status_code.CONFLICT)
            elif acesso == 'admin':
                cookie = request.cookies
                cookie = jwt.decode(cookie['jwt_token'], jwt_secret, algorithms='HS256')
                if database.check_acess(cookie['name']) == 'sudo':
                    try:
                        database.create_user(name, passwd, acesso)
                    except ValueError:
                        return Response('Unable to create admin', status=status_code.INTERNAL_SERVER_ERROR)
                    else:
                        return Response('Admin user was created', status=status_code.CREATED)
                else:
                    return Response('Unauthorized Acess', status=status_code.UNAUTHORIZED)
            else:
                try:
                    database.create_user(name, passwd, acesso) #type: ignore
                except ValueError:
                    return Response('Unable to create user', status=status_code.INTERNAL_SERVER_ERROR)
                else:
                    return Response('User was Created', status=status_code.CREATED)
        else:
            return Response('Method not Allowed', status=status_code.METHOD_NOT_ALLOWED)

    @app.route('/nuke')
    def nuke():
        database.nuke()
        return 'done'
    
    @app.route('/create')
    def create():
        database.create_table()
        return 'done'
    
def check_cookie(cookie, acess_req):
    token = jwt.decode(cookie['jwt_token'], jwt_secret, algorithms='HS256')
    if token['acesso'] == acess_req or token['acesso'] == 'sudo':
        return True
    else:
        return False
    
def check_identity(cookie, id):
    token = jwt.decode(cookie['jwt_token'], jwt_secret, algorithms='HS256')
    return f'{database.check_identity(token['name'])}'

main()