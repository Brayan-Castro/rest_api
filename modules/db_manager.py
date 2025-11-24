from dotenv import load_dotenv
import pymysql
import os
load_dotenv(dotenv_path='./.env')

_TABLE_NAME = "rest_table"

"""
    if returning a value aka returning all users or user by id, use dictcursor to get the answer as a dict
"""

def sql_connection():
    return pymysql.connect(
        host = os.getenv('MYSQL_HOST'),
        user = os.getenv('MYSQL_USER'),
        password = os.getenv('MYSQL_PASSWORD'), # type: ignore
        database = os.getenv('MYSQL_DATABASE')
    ) # type: ignore

def nuke():
    with sql_connection() as con:
        with con.cursor() as cur:
            cur.execute(f'DROP TABLE {_TABLE_NAME}')
            con.commit()

def create_table():
    with sql_connection() as con:
        with con.cursor() as cur:
            cur.execute(f"CREATE TABLE IF NOT EXISTS {_TABLE_NAME} (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, acesso VARCHAR(255) NOT NULL)")

def create_user(name:str, passwd:str, acesso:str):
    # /users with [POST]
    with sql_connection() as con:
        with con.cursor() as cur:
            cur.execute(f'SELECT username FROM {_TABLE_NAME} where username = %s', (name))
            user = cur.fetchone()
            if type(user) != type(None):
                raise ValueError('User already exists')
            else:
                cur.execute(f"INSERT INTO {_TABLE_NAME} (username, password, acesso) values (%s, %s, %s)", (name, passwd, acesso))
                con.commit()

def remove_user(name:str = '', passwd:str = '', id:int= 0):
    with sql_connection() as con:
        with con.cursor() as cur:
            if id != 0:
                cur.execute(f"SELECT FROM {_TABLE_NAME} WHERE username = %s AND password = %s", (name, passwd))
                user = cur.fetchone()
                if type(user) != type(None):
                    cur.execute(f"DELETE FROM {_TABLE_NAME} WHERE username = %s AND password = %s", (name, passwd))
                    con.commit()
                else:
                    raise ValueError('User not found')
            else:
                cur.execute(f"SELECT FROM {_TABLE_NAME} WHERE id = %s", (id))
                user = cur.fetchone()
                if type(user) != type(None):
                    cur.execute(f"DELETE FROM {_TABLE_NAME} WHERE id = %s", (id))
                    con.commit()
                else:
                    raise ValueError('User not found')

def see_user(id = 0, name = '', passwd = ''):
    with sql_connection() as con:
        with pymysql.cursors.DictCursor(con) as cur:
            if id:
                # /users/<id> with [GET]
                cur.execute(f'SELECT * FROM {_TABLE_NAME} WHERE id = %s', (id))
                user = cur.fetchone()
                if type(user) != type(None):
                    return user
                else:
                    raise ValueError('User not found')
            elif name != '' and passwd != '':
                cur.execute(f'SELECT * FROM {_TABLE_NAME} WHERE username = %s AND password = %s', (name, passwd))
                user = cur.fetchone()
                if type(user) != type(None):
                    return user
                else:
                    raise ValueError('User not found')
            else:
                # /users with [GET]
                cur.execute(f'SELECT * FROM {_TABLE_NAME}')
                user = cur.fetchall()
                if len(user) > 0:
                    return user
                else:
                    raise ValueError('Database is empty')
                
def check_identity(name):
    with sql_connection() as con:
        with con.cursor() as cur:
            cur.execute(f'SELECT id FROM {_TABLE_NAME} WHERE username = %s', (name))
            return cur.fetchone()
                
def check_sudo():
    with sql_connection() as con:
        with con.cursor() as cur:
            cur.execute(f'SELECT username FROM {_TABLE_NAME} WHERE acesso = %s', ('sudo'))
            sudo = cur.fetchone()
            if type(sudo) != type(None):
                return False
            else:
                return True
            
def check_acess(name:str):
    with sql_connection() as con:
        with con.cursor() as cur:
            cur.execute(f'SELECT acesso FROM {_TABLE_NAME} WHERE username = %s', (name))
            return cur.fetchone()[0] #type: ignore