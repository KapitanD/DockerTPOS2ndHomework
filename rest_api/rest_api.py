from flask import Flask, jsonify, json
import psycopg2
from psycopg2.extras import DictCursor
from psycopg2 import sql
from contextlib import closing
import time
import os

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')

app = Flask(__name__)

# waiting for postgresql db
while True:
    try:
        psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                         password=DB_PASSWORD, host=DB_HOST)
        break
    except psycopg2.OperationalError:
        time.sleep(1)


@app.errorhandler(404)
def page_not_found(e):
    return app.response_class(
        status=404,
        mimetype='application/json',
        response=json.dumps({"error":"Not found"})
    )



@app.route('/')
def get_data():
    with closing(psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                                  password=DB_PASSWORD, host=DB_HOST)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            conn.autocommit = True
            cursor.execute("SELECT str_field, number_field from data;")
            data = [row for row in cursor]
            return jsonify(data)


@app.route('/health')
def hello_health():
    return app.response_class(
        status=200
    )


if __name__ == '__main__':
    app.run(host="rest_api.out", port=1234)
