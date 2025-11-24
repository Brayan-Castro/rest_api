# Backend User-Control REST API
Simple REST API made using Flask and MySQL for user-control (Authentication, Authorization and CRUD (minus de U for now))

## Frameworks Used

#### Flask
The main component used for the API itself.

#### MySQL / PyMySQL
The second main component, used for the database and communicating changes to the database.

#### PyJWT
Used for Authorization and Authentication inside the API.

#### Docker
Used for hosting both the MySQL Server and the API.

#### Python-Dotenv
Used for securing sensitive data (jwt secret and database login information)

## Endpoints
Currently there are 2 main endpoints, the branches and methods allowed by these endpoints are:

### /auth/
#### /auth/register [POST]
Used for user/admin/sudo registration, requires a JSON Payload with name, password and acess level, additionaly, may require a JWT Cookie with sudo acess level for creating admins.

#### /auth/login [GET]
As the name implies it's used for login, returns a JWT Encoded cookie containing name and acess level, this cookie lasts until session expires and may be saved and sent back as Authentication for other endpoints

### /api/
#### /api/users [GET]
This endpoint has several uses, it accepts (but not obligatory) a JSON Payload containing name and password, it may also require the JWT Cookie; Sending a [GET] request with no JSON Payload returns all the user data inside the database but requires a JWT Cookie with admin acess level, sending a [GET] request with a JSON Payload returns only the data associated with the name and password in the JSON and doesn't require a JWT Cookie.
#### /api/users [DELETE]
Requires both a JSON Payload and a JWT with admin acess, this endpoint tries to delete from the database the user specified inside the JSON Payload.

#### /api/users/<int:id> [GET] [DELETE]
Requires both a JSON Payload and a JWT with admin acess, if used with a [GET] request, returns used data with the associated id, if used with a [DELETE] request, tries to delete the user with the associated id.

### /nuke
Nukes the database table (FOR TESTING PURPOSES)

### /create
Recreates the database table (FOR TESTING PURPOSES)

## Other
### Acess Level Permissions
Sudo > Admin > User \
There can only be one sudo on the database, and only he can create other admins

### HTTP Responses
(Most) Errors won't crash the API but will return an appropriate HTTP Response, inside the main API code (rest_api.py), every code is called from another python module (modules/status.py) for clarity (so inside the code it doesn't appear as 401, but status_code.UNAUTHORIZED)

### JSON Payload
This is a sample payload accepted by the API:
{'name': 'user1', 'passwd': '123', 'acesso': 'admin'}