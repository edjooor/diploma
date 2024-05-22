from flask import render_template, flash, redirect, url_for
from app import app
import psycopg2, os, jinja2


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='earthquakes_map',
                            user='postgres',
                            password='1234')
                            
    return conn



@app.route('/')
@app.route('/index')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM s1;')
    earthquakes_S1 = cur.fetchall()
    cur.close()
    conn.close()  
    return render_template('index.html', title='Earthquake map', earthquakes_S1=earthquakes_S1)

@app.route('/earthquake/<int:earthquake_id>')
def earthquake_detail(earthquake_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM s1 WHERE id = %s;', (earthquake_id,))
    earthquake = cur.fetchone()
    cur.close()
    conn.close()
    if earthquake is None:
        return "Earthquake not found", 404
    return render_template('earthquake_detail.html', earthquake=earthquake)