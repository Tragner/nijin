from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import hashlib
import time
import unicodedata

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/nijin'
db = SQLAlchemy(app)

# Team
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(80), unique=True)
    mate_email = db.Column(db.String(80))
    password = db.Column(db.String(32))
    active = db.Column(db.Boolean())
    token = db.Column(db.String(32))
    project = db.relationship('Project', backref='team', lazy='dynamic')

    def __init__(self, name, email, mate_email, password):
        self.name = name
        self.email = email
        self.mate_email = mate_email
        self.password = hashlib.md5(password.encode('utf-8')).hexdigest()
        self.active = False
        self.token = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()

    def __repr__(self):
        return '<Team {0}>'.format(self.email)
# Project
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    image = db.Column(db.String(500))
    brief = db.relationship('Brief', backref='project', lazy='dynamic')
    resource = db.relationship('Resource', backref='project', lazy='dynamic')
    brainstorm = db.relationship('Brainstorm', backref='project', lazy='dynamic')
    sketch = db.relationship('Sketch', backref='project', lazy='dynamic')
    solution = db.relationship('Solution', backref='project', lazy='dynamic')
    id_team = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __init__(self, name, ruta, id_team):
        self.name = name
        self.image = ruta
        self.id_team = id_team

    def __repr__(self):
        return '<Project %r>' % self.name

# Briefing
class Brief(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    what_id = db.Column(db.Integer, db.ForeignKey('what.id'))
    what_txt = db.Column(db.String(200))
    who_id = db.Column(db.Integer, db.ForeignKey('who.id'))
    who_txt = db.Column(db.String(200))
    when = db.Column(db.Integer)
    when_txt = db.Column(db.String(200))
    id_project = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __init__(self, what, what_txt, who, who_txt, when, when_txt, id_project):
        self.what = what
        self.what_txt = what_txt
        self.who = who
        self.who_txt = who_txt
        self.when = when
        self.when_txt = when_txt
        self.id_project = id_project

    def __repr__(self):
        return '<Brief %r>' % self.what_txt

class What(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    brief = db.relationship('Brief', backref='what', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<What %r>' % self.name


class Who(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    brief = db.relationship('Brief', backref='who', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Who %r>' % self.name

# Resources
class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.UnicodeText())
    label = db.Column(db.String(80))
    like = db.Column(db.Integer)
    id_project = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __init__(self, link, label, id_project):
        self.link = link
        self.label = label
        self.like = 0
        self.id_project = id_project

    def __repr__(self):
        return '<Resource %r>' % self.label

# Brainstorm
class Brainstorm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(20))
    like = db.Column(db.Integer)
    id_project = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __init__(self, word, label, id_project):
        self.word = word
        self.label = label
        self.like = 0
        self.id_project = id_project

    def __repr__(self):
        return '<Brainstorm %r>' % self.word

# Sketching
class Sketch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_sketch_id = db.Column(db.Integer, db.ForeignKey('first_sketch.id'))
    second_sketch_id = db.Column(db.Integer, db.ForeignKey('second_sketch.id'))
    third_sketch_id = db.Column(db.Integer, db.ForeignKey('third_sketch.id'))
    id_project = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __init__(self, first_sketch, second_sketch, third_sketch, id_project):
        self.first_sketch = first_sketch
        self.second_sketch = second_sketch
        self.third_sketch = third_sketch
        self.id_project = id_project

    def __repr__(self):
        return '<Brainstorm %r>' % self.id_project

class First_sketch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    image = db.Column(db.String(500))
    like = db.Column(db.Integer)
    sketch = db.relationship('Sketch', backref='first_sketch', lazy='dynamic')

    def __init__(self, name, ruta):
        self.name = name
        self.image = ruta
        self.like = 0

    def __repr__(self):
        return '<First_sketch %r>' % self.name

class Second_sketch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    image = db.Column(db.String(500))
    like = db.Column(db.Integer)
    sketch = db.relationship('Sketch', backref='second_sketch', lazy='dynamic')

    def __init__(self, name, ruta):
        self.name = name
        self.image = ruta
        self.like = 0

    def __repr__(self):
        return '<Second_sketch %r>' % self.name

class Third_sketch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    image = db.Column(db.String(500))
    like = db.Column(db.Integer)
    sketch = db.relationship('Sketch', backref='third_sketch', lazy='dynamic')

    def __init__(self, name, ruta):
        self.name = name
        self.image = ruta
        self.like = 0

    def __repr__(self):
        return '<Third_sketch %r>' % self.name

class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    image = db.Column(db.String(500))
    like = db.Column(db.Integer)
    id_project = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __init__(self, name, ruta):
        self.name = name
        self.image = ruta
        self.like = 0
        self.id_project = id_project

    def __repr__(self):
        return '<Solution %r>' % self.name