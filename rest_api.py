from flask import Flask, Response, make_response, jsonify
from flask import request
import modules.db_manager as database
import modules.status as status_code
app = Flask(__name__)

"""
endpoints
    /users <return all user (names) [GET] (done)
    /users/<id> return user with especified id (and a random email, will do these later) [GET] (done)
    /users [POST] <creater a new user (will think of a way of sending the passwd later) (done)
    /users/<id> [DELETE] <deletes the user with the specified id
    /users/<id> [PATCH] <update user info
"""

def main():
    @app.route("/api/users", methods=['GET', 'POST', 'DELETE']) #type: ignore
    def return_users():
        if request.method == 'GET':
            try:
                return database.see_user()
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
                return database.see_user(id)
            except ValueError:
                return Response('User not found', status=status_code.NO_CONTENT)
            
    @app.route('/cook')
    def cook():
        response = make_response(jsonify({'buceta': 'rosa'}))
        response.set_cookie('teste', value='caralhoooo')
        response.set_cookie('user', value='nerda')
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
    

# @app.route("/cringe")
# def noia_page():
#     return 'cringe'

# @app.route("/")
# def index_page():
#     return "siu"

main()