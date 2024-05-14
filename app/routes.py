from flask import render_template, flash, redirect, url_for
from app import app
import psycopg2, os, jinja2


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='earthquakes_map',
                            user='postgres',
                            password='1234')
                            # user=os.environ['postgres'],
                            # password=os.environ['1234'])
    return conn



@app.route('/')
@app.route('/index')
def index():

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM s1;')
    earthquakes_S1 = cur.fetchall()
    # print(earthquakes)
    cur.close()
    conn.close()
   
    # earthquakes = [
    #     {
    #         'date': {'date': '3/13/1990'},
    #         'time': {'time': '05:36:01.01'},
    #     },
    #     {
    #         'date': {'date': '4/12/1985'},
    #         'time': {'time': '00:33:01.01'},
            
    #     }
    # ]
    return render_template('index.html', title='Earthquake map', earthquakes_S1=earthquakes_S1)
