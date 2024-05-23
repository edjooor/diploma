from flask import render_template, flash, redirect, url_for
from app import app
import psycopg2, os, jinja2
import matplotlib.pyplot as plt
import obspy.imaging.beachball as beachball


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='earthquakes_map',
                            user='postgres',
                            password='1234')                            
    return conn


# def draw_beachballs():
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute('SELECT * FROM s1;')
#     earthquakes_S1 = cur.fetchall()  
#     i=0
#     print(i)
#     while int(i) < int(len(earthquakes_S1)):
#         fig = plt.figure(figsize=(7, 7) )
#         ax = fig.add_subplot(111, aspect='equal')
#         bb = beachball.beach((int(earthquakes_S1[i][14]), int(earthquakes_S1[i][15]), int(earthquakes_S1[i][16])), facecolor='k',width=400, axes=ax, xy=(0.5, 0.5) )
#         ax.add_collection(bb)
#         pathto = 'stat/beachball_'
#         pathto += str(earthquakes_S1[i][0]) + '.png'
#         plt.savefig(pathto)
#         i+=1
# draw_beachballs()


@app.route('/')
# @app.route('/index')
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