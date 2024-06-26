
from flask import render_template, flash, redirect, url_for, request
from app import app
import psycopg2, os, jinja2
import matplotlib.pyplot as plt
import obspy.imaging.beachball as beachball
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired
import mysql.connector



app.secret_key = 'your_secret_key'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Dummy user database
users = {'admin': {'password': 'adminpass'}}

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EditForm(FlaskForm):
    eq_date = StringField('Дата:', validators=[DataRequired()])  
    eq_time = StringField('Время:', validators=[DataRequired()]) 
    lattitude_deg = StringField('Широта:', validators=[DataRequired()]) 
    longtitude_deg = StringField('Долгота:', validators=[DataRequired()]) 
    n =  StringField('N:', validators=[DataRequired()]) 
    delta_min =  StringField('Δmin, deg:', validators=[DataRequired()]) 
    delta_max = StringField('Δmax, deg:', validators=[DataRequired()]) 
    period_range = StringField('Period range, s:', validators=[DataRequired()]) 
    crustal_model = StringField('Crustal model:', validators=[DataRequired()]) 
    residual = StringField('ε:', validators=[DataRequired()]) 
    magnitude = StringField('Magnitude:', validators=[DataRequired()]) 
    moment_0 = StringField('Mo, N m:', validators=[DataRequired()]) 
    h_depth = StringField('h, km:', validators=[DataRequired()]) 
    np1_azm = StringField('Nodal plane 1, azm, deg:', validators=[DataRequired()]) 
    np1_dp = StringField('Nodal plane 1, dp, deg:', validators=[DataRequired()]) 
    np1_slip = StringField('Nodal plane 1, slip,deg:', validators=[DataRequired()]) 
    np2_azm = StringField('Nodal plane 2, azm, deg:', validators=[DataRequired()]) 
    np2_dp = StringField('Nodal plane 2, dp, deg:', validators=[DataRequired()]) 
    np2_slip = StringField('Nodal plane 2, slip, deg:', validators=[DataRequired()]) 
    t_axis_azm = StringField('T axis, azm, deg:', validators=[DataRequired()]) 
    t_axis_pl = StringField('T axis, pl, deg:', validators=[DataRequired()]) 
    p_axis_azm = StringField('P axis, azm, deg:', validators=[DataRequired()]) 
    p_axis_pl = StringField('P axis, pl, deg:', validators=[DataRequired()]) 
    b_axis_azm = StringField('B axis, azm, deg:', validators=[DataRequired()]) 
    b_axis_pl = StringField('B axis, pl, deg:', validators=[DataRequired()]) 
    reference = StringField('Название:', validators=[DataRequired()]) 

    n_s2 =  StringField('N:', validators=[DataRequired()]) 
    delta_min_s2 =  StringField('Δmin, deg:', validators=[DataRequired()]) 
    delta_max_s2 = StringField('Δmax, deg:', validators=[DataRequired()]) 
    period_range_s2 = StringField('Period range, s:', validators=[DataRequired()]) 
    residual_s2 = StringField('ε:', validators=[DataRequired()]) 
    moment_0_s2 = StringField('Mo, N m:', validators=[DataRequired()]) 
    h_depth_s2 = StringField('h, km:', validators=[DataRequired()]) 
    IntegralCharacteristics_delta_t_s2 = StringField('Δt, s:', validators=[DataRequired()]) 
    IntegralCharacteristics_l_max_s2 = StringField('lmax, km:', validators=[DataRequired()]) 
    IntegralCharacteristics_l_min_s2 = StringField('lmin, km:', validators=[DataRequired()]) 
    IntegralCharacteristics_v_speed_s2 = StringField('v, km/s:', validators=[DataRequired()]) 
    IntegralCharacteristics_f_1_s2 = StringField('ϕ1, °:', validators=[DataRequired()]) 
    IntegralCharacteristics_f_v_s2 = StringField('ϕv, °:', validators=[DataRequired()]) 
    rupture_plane_s2 = StringField('Rupture plane:', validators=[DataRequired()]) 
    bilateral_model_s2 = StringField('Bilateral model:', validators=[DataRequired()]) 
    reference_s2 = StringField('Reference:', validators=[DataRequired()]) 

    submit = SubmitField('Сохранить изменения')

class AddEarthquakeForm(FlaskForm):
    eq_date = StringField('Дата:', validators=[DataRequired()])  
    eq_time = StringField('Время:', validators=[DataRequired()]) 
    lattitude_deg = StringField('Широта:', validators=[DataRequired()]) 
    longtitude_deg = StringField('Долгота:', validators=[DataRequired()]) 
    n =  StringField('N:', validators=[DataRequired()]) 
    delta_min =  StringField('Δmin, deg:', validators=[DataRequired()]) 
    delta_max = StringField('Δmax, deg:', validators=[DataRequired()]) 
    period_range = StringField('Period range, s:', validators=[DataRequired()]) 
    crustal_model = StringField('Crustal model:', validators=[DataRequired()]) 
    residual = StringField('ε:', validators=[DataRequired()]) 
    magnitude = StringField('Magnitude:', validators=[DataRequired()]) 
    moment_0 = StringField('Mo, N m:', validators=[DataRequired()]) 
    h_depth = StringField('h, km:', validators=[DataRequired()]) 
    np1_azm = StringField('Nodal plane 1, azm, deg:', validators=[DataRequired()]) 
    np1_dp = StringField('Nodal plane 1, dp, deg:', validators=[DataRequired()]) 
    np1_slip = StringField('Nodal plane 1, slip,deg:', validators=[DataRequired()]) 
    np2_azm = StringField('Nodal plane 2, azm, deg:', validators=[DataRequired()]) 
    np2_dp = StringField('Nodal plane 2, dp, deg:', validators=[DataRequired()]) 
    np2_slip = StringField('Nodal plane 2, slip, deg:', validators=[DataRequired()]) 
    t_axis_azm = StringField('T axis, azm, deg:', validators=[DataRequired()]) 
    t_axis_pl = StringField('T axis, pl, deg:', validators=[DataRequired()]) 
    p_axis_azm = StringField('P axis, azm, deg:', validators=[DataRequired()]) 
    p_axis_pl = StringField('P axis, pl, deg:', validators=[DataRequired()]) 
    b_axis_azm = StringField('B axis, azm, deg:', validators=[DataRequired()]) 
    b_axis_pl = StringField('B axis, pl, deg:', validators=[DataRequired()]) 
    reference = StringField('Название:', validators=[DataRequired()]) 

    n_s2 =  StringField('N:', validators=[DataRequired()]) 
    delta_min_s2 =  StringField('Δmin, deg:', validators=[DataRequired()]) 
    delta_max_s2 = StringField('Δmax, deg:', validators=[DataRequired()]) 
    period_range_s2 = StringField('Period range, s:', validators=[DataRequired()]) 
    residual_s2 = StringField('ε:', validators=[DataRequired()]) 
    moment_0_s2 = StringField('Mo, N m:', validators=[DataRequired()]) 
    h_depth_s2 = StringField('h, km:', validators=[DataRequired()]) 
    IntegralCharacteristics_delta_t_s2 = StringField('Δt, s:', validators=[DataRequired()]) 
    IntegralCharacteristics_l_max_s2 = StringField('lmax, km:', validators=[DataRequired()]) 
    IntegralCharacteristics_l_min_s2 = StringField('lmin, km:', validators=[DataRequired()]) 
    IntegralCharacteristics_v_speed_s2 = StringField('v, km/s:', validators=[DataRequired()]) 
    IntegralCharacteristics_f_1_s2 = StringField('ϕ1, °:', validators=[DataRequired()]) 
    IntegralCharacteristics_f_v_s2 = StringField('ϕv, °:', validators=[DataRequired()]) 
    rupture_plane_s2 = StringField('Rupture plane:', validators=[DataRequired()]) 
    bilateral_model_s2 = StringField('Bilateral model:', validators=[DataRequired()]) 
    reference_s2 = StringField('Reference:', validators=[DataRequired()]) 


    
    
    submit = SubmitField('Добавить землетрясение')


# def get_db_connection():
#     conn = psycopg2.connect(
#         host='localhost',
#         database='earthquakes_map',
#         user='postgres',
#         password='1234'
#     )
#     return conn
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        database='earthquakes',
        user='root',
        password='password'
    )
    return conn
def draw_beachballs():    
    base_path = os.path.abspath(os.path.dirname(__file__))
    pathto_dir = os.path.join(base_path, 'static', 'beachballs')
    
    if not os.path.exists(pathto_dir):
        os.makedirs(pathto_dir)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM s1;')
    earthquakes_S1 = cur.fetchall()
    i = 0
    while i < len(earthquakes_S1):
        fig = plt.figure(figsize=(7, 7))
        ax = fig.add_subplot(111, aspect='equal')
        bb = beachball.beach(
            (float(earthquakes_S1[i][14]), float(earthquakes_S1[i][15]), float(earthquakes_S1[i][16])),
            facecolor='k',
            width=400,
            axes=ax,
            
            xy=(0.5, 0.5)
        )
        ax.add_collection(bb)
        pathto = os.path.join(pathto_dir, f'beachball_{earthquakes_S1[i][0]}.png')
        plt.savefig(pathto)
        plt.close(fig)  
        i += 1

draw_beachballs()




@app.route('/')
# @app.route('/index')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM s1;')
    earthquakes_S1 = cur.fetchall()
    cur.close()
    conn.close()
    earthquake_detail_url = url_for('earthquake_detail', earthquake_id=0).rsplit('/', 1)[0] + '/'
    return render_template('index.html', earthquakes_S1=earthquakes_S1, earthquake_detail_url=earthquake_detail_url)  
    # return render_template('index.html', title='Earthquake map', earthquakes_S1=earthquakes_S1)

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM s1;')
    earthquakes_S1 = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin.html', title='Admin', earthquakes_S1=earthquakes_S1)

@app.route('/edit/<int:earthquake_id>', methods=['GET', 'POST'])
@login_required
def edit(earthquake_id):
    form = EditForm()
    if form.validate_on_submit():
        eq_date = form.eq_date.data
        eq_time = form.eq_time.data
        lattitude_deg = form.lattitude_deg.data
        longtitude_deg = form.longtitude_deg.data
        n = form.n.data
        delta_min = form.delta_min.data
        delta_max = form.delta_max.data
        period_range = form.period_range.data
        crustal_model = form.crustal_model.data
        residual = form.residual.data
        magnitude = form.magnitude.data
        moment_0 = form.moment_0.data
        h_depth = form.h_depth.data
        np1_azm = form.np1_azm.data
        np1_dp = form.np1_dp.data
        np1_slip = form.np1_slip.data
        np2_azm = form.np2_azm.data
        np2_dp = form.np2_dp.data
        np2_slip = form.np2_slip.data
        t_axis_azm = form.t_axis_azm.data
        t_axis_pl = form.t_axis_pl.data
        p_axis_azm = form.p_axis_azm.data
        p_axis_pl = form.p_axis_pl.data
        b_axis_azm = form.b_axis_azm.data
        b_axis_pl = form.b_axis_pl.data
        reference = form.reference.data

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE s1 SET eq_date = %s, eq_time = %s, lattitude_deg = %s, longtitude_deg = %s, n = %s, delta_min = %s, delta_max = %s, period_range = %s, crustal_model = %s, residual = %s, magnitude = %s, moment_0 = %s, h_depth = %s, np1_azm = %s, np1_dp = %s, np1_slip = %s, np2_azm = %s, np2_dp = %s,	np2_slip = %s, t_axis_azm = %s, t_axis_pl = %s, p_axis_azm = %s, p_axis_pl = %s, b_axis_azm = %s, b_axis_pl = %s, reference = %s, WHERE id = %s', (eq_date, eq_time, lattitude_deg, longtitude_deg, n, delta_min, delta_max, period_range, 
                             crustal_model, residual, magnitude, moment_0, h_depth, np1_azm, np1_dp, np1_slip, np2_azm, 
                             np2_dp, np2_slip, t_axis_azm, t_axis_pl, p_axis_azm, p_axis_pl, b_axis_azm, b_axis_pl, reference, earthquake_id))
        conn.commit()
        cur.close()
        conn.close()
        flash('Changes saved successfully')
        draw_beachballs()
        return redirect(url_for('admin'))
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM s1 WHERE id = %s;', (earthquake_id,))
    earthquake = cur.fetchone()
    cur.close()
    conn.close()
    
    if earthquake is None:
        return "Earthquake not found", 404
    
    form.eq_date.data = earthquake[1]  
    form.eq_time.data = earthquake[2]  
    form.lattitude_deg.data = earthquake[3]  
    form.longtitude_deg.data = earthquake[4]  
    form.n.data = earthquake[5]  
    form.delta_min.data = earthquake[6]  
    form.delta_max.data = earthquake[7]  
    form.period_range.data = earthquake[8]  
    form.crustal_model.data = earthquake[9]  
    form.residual.data = earthquake[10]  
    form.magnitude.data = earthquake[11]  
    form.moment_0.data = earthquake[12]  
    form.h_depth.data = earthquake[13]  
    form.np1_azm.data = earthquake[14]  
    form.np1_dp.data = earthquake[15]  
    form.np1_slip.data = earthquake[16]  
    form.np2_azm.data = earthquake[17]  
    form.np2_dp.data = earthquake[18]  
    form.np2_slip.data = earthquake[19]  
    form.t_axis_azm.data = earthquake[20]  
    form.t_axis_pl.data = earthquake[21]  
    form.p_axis_azm.data = earthquake[22]  
    form.p_axis_pl.data = earthquake[23]  
    form.b_axis_azm.data = earthquake[24]  
    form.b_axis_pl.data = earthquake[25]  
    form.reference.data = earthquake[26]  

    
    return render_template('edit.html', title='Edit Earthquake', form=form)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_earthquake():
    form = AddEarthquakeForm()
    if request.method == 'POST':
        print("Form submitted.")  
        print("Field1:", form.eq_date.data)
        print("Field2:", form.eq_time.data)
    
        
        if form.validate_on_submit():
            eq_date = form.eq_date.data
            eq_time = form.eq_time.data
            lattitude_deg = form.lattitude_deg.data
            longtitude_deg = form.longtitude_deg.data
            n = form.n.data
            delta_min = form.delta_min.data
            delta_max = form.delta_max.data
            period_range = form.period_range.data
            crustal_model = form.crustal_model.data
            residual = form.residual.data
            magnitude = form.magnitude.data
            moment_0 = form.moment_0.data
            h_depth = form.h_depth.data
            np1_azm = form.np1_azm.data
            np1_dp = form.np1_dp.data
            np1_slip = form.np1_slip.data
            np2_azm = form.np2_azm.data
            np2_dp = form.np2_dp.data
            np2_slip = form.np2_slip.data
            t_axis_azm = form.t_axis_azm.data
            t_axis_pl = form.t_axis_pl.data
            p_axis_azm = form.p_axis_azm.data
            p_axis_pl = form.p_axis_pl.data
            b_axis_azm = form.b_axis_azm.data
            b_axis_pl = form.b_axis_pl.data
            reference = form.reference.data
            
            
            print("Form data received:", eq_date, eq_time)  
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                get_id = cur.execute('SELECT MAX(id) FROM s1;')
                print(cur.execute('SELECT MAX(id) FROM s1;'))
                # Insert into s1
                cur.execute('INSERT INTO s1 (eq_date, eq_time,lattitude_deg, longtitude_deg, n, delta_min, delta_max, period_range, crustal_model, residual, magnitude, moment_0, h_depth, np1_azm, np1_dp, np1_slip, np2_azm, np2_dp,	np2_slip, t_axis_azm, t_axis_pl, p_axis_azm, p_axis_pl,	b_axis_azm,	b_axis_pl, reference) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id',
                            (eq_date, eq_time, lattitude_deg, longtitude_deg, n, delta_min, delta_max, period_range, 
                             crustal_model, residual, magnitude, moment_0, h_depth, np1_azm, np1_dp, np1_slip, np2_azm, 
                             np2_dp, np2_slip, t_axis_azm, t_axis_pl, p_axis_azm, p_axis_pl, b_axis_azm, b_axis_pl, reference))
                new_id = cur.fetchone()[0]
                print("New ID generated:", new_id)  
                # Insert into s2 using the new id
                cur.execute('INSERT INTO s2 (earthquake_id) VALUES (%s)', (new_id,))
                conn.commit()
                cur.close()
                conn.close()
                flash('New earthquake added successfully')
                draw_beachballs()
            except Exception as e:
                print("Error occurred:", e)  
                flash(f'An error occurred: {e}')
                if conn:
                    conn.rollback()
            return redirect(url_for('admin'))
        else:
            print("Form validation failed.")  
            print("Errors:", form.errors)  
    return render_template('add.html', title='Add Earthquake', form=form)

