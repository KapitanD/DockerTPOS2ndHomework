import psycopg2
from psycopg2.extras import DictCursor
from psycopg2 import sql
import csv
import os
from contextlib import closing
import time


DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')

with open('./data/data.csv') as data_file:
    reader = csv.reader(data_file, delimiter=';')
    while True:
        try:
            psycopg2.connect(dbname=DB_NAME, user=DB_USER, 
                 password=DB_PASSWORD, host=DB_HOST)
            break
        except psycopg2.OperationalError:
            time.sleep(1)
            
    with closing(psycopg2.connect(dbname=DB_NAME, user=DB_USER, 
                 password=DB_PASSWORD, host=DB_HOST)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            conn.autocommit = True
            cursor.execute("""
                    CREATE TABLE data (
                        id          SERIAL PRIMARY KEY,
                        str_field        varchar(200),
                        number_field       integer
                    );""")
            values = [(row[0], row[1]) for row in reader]
            for row in reader:
                cursor.execute(f"""
                INSERT INTO data(str_field, number_field)
                VALUES({row[0]}, {row[1]})
                ;""")
            insert = sql.SQL('INSERT INTO data (str_field, number_field) VALUES {}').format(
                             sql.SQL(',').join(map(sql.Literal, values)))
            cursor.execute(insert)
            cursor.execute("SELECT * from data;")
            is_okay = True
            for response_row, request_row in zip(cursor, values):
                if response_row['str_field'] != request_row[0] and response_row['nimber_field'] == request_row[1]:
                    is_okay = False

            if is_okay:
                print('data stored to database')
            else:
                print('something went wrong')
