import os
import time
import datetime

from flask import Flask, Response
from flask import send_from_directory
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager

import psycopg2
from psycopg2 import pool

app = Flask(__name__)
app.secret_key = '5w3v5cu42gs6g7tf'

# key = os.environ.get('JWT_SECRET', '2iz45w3v5cu42gvypjj5')
# int_code = os.environ.get('INTERNAL_CODE', '1234')
# app.config["JWT_SECRET_KEY"] = key
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=10)
# jwt = JWTManager(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

DB_NAME = os.environ.get('POSTGRES_USER', 'temp-user')
DB_HOST = os.environ.get('POSTGRES_HOST','34.87.41.115')
DB_USER = os.environ.get('POSTGRES_USER', 'temp-user')
DB_PASS = os.environ.get('POSTGRES_PASSWORD','unicorn_unicorn')
DB_PORT = os.environ.get('POSTGRES_PORT','5432')

conn_pool = psycopg2.pool.ThreadedConnectionPool (
    1,
    2,
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    dbname=DB_NAME,
    port=DB_PORT)

print("Database connction established")

class DB():
    # def __init__ (self,num):
    #     self.num = num

    def run(self, query, args=()):
        global conn_pool
        conn = self._getConnection()

        if conn is None:
            print("EXIT from db.run")
            self.recon()

        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(query, args)
        cur.close ()
        conn_pool.putconn(conn)
        return True

    def execute(self, query, args=()):
        global conn_pool
        conn = self._getConnection()

        if conn is None:
            print("EXIT from db.execute")
            self.recon()

        cur = conn.cursor()
        cur.execute(query, args)
        result = cur.fetchone()
        cur.close()
        conn_pool.putconn(conn)
        return result

    def query_db(self, query, args=(), one=False):
        global conn_pool
        conn = self._getConnection()

        if conn is None:
            print("EXIT from db.querydb")
            self.recon()

        cur = conn.cursor()
        cur.execute(query, args)
        r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
        result = (r[0] if r else None) if one else r
        cur.close()
        conn_pool.putconn(conn)
        return result


    def recon(self):
        global conn_pool
        conn_pool = psycopg2.pool.ThreadedConnectionPool (
                    1,
                    2,
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASS,
                    dbname=DB_NAME,
                    port=DB_PORT)

    def _getConnection(self):
        global conn_pool

        while 1:
            conn = None
            if not conn_pool:
                time.sleep(1)
                self.recon()            
                continue
            try:
                conn = conn_pool.getconn()
            except psycopg2.pool.PoolError:
                time.sleep(1)
            except (psycopg2.InterfaceError, psycopg2.OperationalError) as e:
                self.recon()
            except Exception as e:
                print("Odd Exception",e)
            if conn:
                return conn

db = DB()

from autho_blueprint import autho
app.register_blueprint(autho, url_prefix="/")

from data_blueprint import data
app.register_blueprint(data, url_prefix="/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 7777)), debug=True)