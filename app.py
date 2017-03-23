from flask import Flask, render_template, redirect, url_for, request, flash, session
from forms import TeamForm
from models import db, Team, Project, Brief, What, Who, Resource, Brainstorm, Sketch, First_sketch, Second_sketch, Third_sketch, Solution
from flask_mail import Mail, Message
from functools import wraps
import configparser
import hashlib
import math

app = Flask(__name__)

# Read .env
config = configparser.ConfigParser()
config.read('.env')
# Config Flask
app.debug = config['DEFAULT']['DEBUG']
app.secret_key = config['DEFAULT']['SECRET_KEY']
# Config Mail
app.config['MAIL_SERVER'] = config['MAIL']['MAIL_SERVER']
app.config['MAIL_PORT'] = config['MAIL']['MAIL_PORT']
app.config['MAIL_USE_SSL'] = config['MAIL']['MAIL_USE_SSL']
app.config['MAIL_USERNAME'] = config['MAIL']['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = config['MAIL']['MAIL_PASSWORD']
app.config['MAIL_DEBUG'] = False

mail = Mail(app)
LIMITE_PELICULAS = 5

@app.route("/")
def index():
    return render_template('items/index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = TeamForm()
    if request.args.get('name') and request.args.get('password'):
        name = request.args.get('name')
        password = hashlib.md5(request.args.get('password').encode('utf-8')).hexdigest()
        my_team = Team.query.filter_by(name=name, password=password).first()
        if my_team:
            # Existe
            session['team'] = my_team.name
            return redirect(url_for('home'))
        else:
            # Mostramos error
            flash('Su email o contraseña no es correcto', 'danger')
    return render_template('items/login.html', form=form)

@app.route('/home')
def home():
    return render_template('items/home.html')

@app.route('/admin/briefing')
def briefing():
    return render_template('items/admin/briefing.html')

@app.route('/close')
def close_session():
    session.clear()
    return redirect(url_for('dashboard'))

@app.route("/new", methods=['GET', 'POST'])
def new():
    form = TeamForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = request.form['name']
            email = request.form['email']
            mate_email = request.form['mate_email']
            password = hashlib.md5(request.form['password'].encode('utf-8')).hexdigest()
            my_team = Team.query.filter_by(name=name).first()
            if not my_team:
                if request.form['password'] == request.form['password2']:
                    my_team = Team(request.form['name'], request.form['email'], request.form['mate_email'], request.form['password'])
                    db.session.add(my_team)
                    try:
                        db.session.commit()
                        # Envio de email
                        msg = Message("Hello",
                                      sender="no-reply@nijin.com",
                                      recipients=[my_team.email])
                        link_token = f'http://localhost:5000/activate/{my_team.token}'
                        msg.html = render_template('emails/access.html', link_token=link_token)
                        mail.send(msg)
                        # Informamos al usuario
                        flash('Confirmar email en su bandeja de entrada', 'success')
                    except:
                        db.session.rollback()
                        flash('Disculpe, ha ocurrido un error', 'danger')
                    return redirect(url_for('new'))
                else:
                    flash('Las contraseñas no coinciden', 'danger')
            else:
                flash('El email ya está registrado', 'danger')
        else:
            todos_errores = form.errors.items()
            for campo, errores in todos_errores:
                for error in errores:
                    flash(error, 'danger')
    return render_template('items/new.html', form=form)

@app.route("/activate/<token>")
def activate(token):
    my_team = Team.query.filter_by(token=token).first()
    if my_team:
        my_team.active = True
        db.session.add(my_team)
        try:
            flash('Su cuenta ha sido activada', 'success')
            db.session.commit()
        except:
            db.session.rollback()
    else:
        flash('Enlace caducado', 'danger')
    return redirect(url_for('new'))

@app.route("/filter")
def filter():
    form = MovieForm()
    form_search = SearchForm();
    name = request.args.get('name')
    year = request.args.get('year')
    movies = Movie.query.filter(Movie.name.like(f'%{name}%')).filter(Movie.year.like(f'%{year}%')).all()
    return render_template('items/emails.html', movies=movies, form=form, form_search=form_search, num_paginas=0)

if __name__ == "__main__":
    app.run(debug=True)
