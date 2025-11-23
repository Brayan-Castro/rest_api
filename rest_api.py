from flask import Flask, Response, make_response, jsonify
from flask import request
import modules.db_manager as database
import modules.status as status_code
import jwt
app = Flask(__name__)

"""
endpoints
    /api/users
    /api/users/<id>
"""

def main():
    @app.route("/api/users", methods=['GET', 'POST', 'DELETE']) #type: ignore
    def return_users():
        """
        How to use?
            Simply acess the endpoint (/api/users) with the desired HTTP Method, currently supports these methods:
                [GET]
                    Returns a JSON with the user data regarding all the users in this database, if the database is empty, it raises an HTTP Response with the code 204.
                [POST]
                    Tries to create a user on the database, requires and additional payload consisting of a JSON file containing a dict with the keys 'name' and 'passwd' with the content-type of 'application/json',
                    on sucess, returns an HTTP Response with the code 201, on failure, returns an HTTP Response with the code 500.
                    request example: session.post("http://127.0.0.1:5000/api/users", headers = {'Content-Type': 'application/json'}, data=json.dumps({'name': 'teste', 'passwd': 'teste'}))
                [DELETE]
                    Tries to remove a user from the database, requires and additional payload consisting of a JSON file containing a dict with the keys 'name' and 'passwd' with the content-type of 'application/json',
                    on sucess, returns an HTTP Response with the code 200, on failure, returns an HTTP Response with the code 204.
                    request example: session.delete("http://127.0.0.1:5000/api/users", headers = {'Content-Type': 'application/json'}, data=json.dumps({'name': 'teste', 'passwd': 'teste'}))

        """
        if request.method == 'GET':
            try:
                return jsonify(database.see_user())
            except ValueError:
                return Response('Database is Empty', status=status_code.NO_CONTENT)
            
        elif request.method == 'POST':
            data = request.json
            name = data['name'] #type: ignore
            passwd = data['passwd'] #type: ignore

            try:
                database.create_user(name, passwd)
                return Response('User was Created', status=status_code.CREATED)
            except ValueError:
                return Response('Unable to create user', status=status_code.INTERNAL_SERVER_ERROR)
            
        elif request.method == 'DELETE':
            data = request.json
            name = data['name'] #type: ignore
            passwd = data['passwd'] #type: ignore

            try:
                database.remove_user(name, passwd)
                return Response('User was deleted', status=status_code.OK)
            except ValueError:
                return Response('User not found', status=status_code.NO_CONTENT)
        
    @app.route('/api/users/<int:id>', methods=['GET', 'DELETE']) #type: ignore
    def return_user_with_id(id):
        if request.method == 'GET':
            try:
                return jsonify(database.see_user(id))
            except ValueError:
                return Response('User not found', status=status_code.NO_CONTENT)
            
    @app.route('/cook')
    def cook():
        response = make_response(jsonify({'pls': 'work'}))
        token = jwt.encode({'teste': 'sim'}, 'nosferatu', algorithm='HS256')
        response.set_cookie('teste', value=token)
        return response
    
    @app.route('/getcook')
    def get_cook():
        return request.cookies
    
    @app.route('/nuke')
    def nuke():
        database.nuke()
        return 'done'
    
    @app.route('/create')
    def create():
        database.create_table()
        return 'done'

main()