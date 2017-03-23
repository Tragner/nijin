from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length, Email, DataRequired, NumberRange
from datetime import datetime

class TeamForm(Form):
    name = StringField('Project Name', validators=[InputRequired('Campo Nombre Obligatorio'),
                                             Length(1, 17, 'Nombre inferior a 17 caracteres. Puedes usar minúsculaMayúscula')])
    email = StringField('Your Email', validators=[InputRequired('Campo Email Obligatorio'),
                                             Length(1, 80, 'Texto inferior a 80 caracteres'),
                                             Email('Correo incorrecto')])
    mate_email = StringField('Mate Email', validators=[InputRequired('Campo Email Obligatorio'),
                                                 Length(1, 80, 'Texto inferior a 80 caracteres'),
                                                 Email('Correo incorrecto')])
    password = PasswordField('Password', validators=[InputRequired('Por favor, escribe una contraseña')])
    password2 = PasswordField('Repeat Password', validators=[InputRequired('Por favor, escribe de nuevo la contraseña')])
    submit = SubmitField('Submit')

class TeamForm(Form):
    name = StringField('Project Name', validators=[InputRequired('Campo Nombre Obligatorio'),
                                             Length(1, 17, 'Nombre inferior a 17 caracteres. Puedes usar minúsculaMayúscula')])
    email = StringField('Your Email', validators=[InputRequired('Campo Email Obligatorio'),
                                             Length(1, 80, 'Texto inferior a 80 caracteres'),
                                             Email('Correo incorrecto')])
    mate_email = StringField('Mate Email', validators=[InputRequired('Campo Email Obligatorio'),
                                                 Length(1, 80, 'Texto inferior a 80 caracteres'),
                                                 Email('Correo incorrecto')])
    password = PasswordField('Password', validators=[InputRequired('Por favor, escribe una contraseña')])
    password2 = PasswordField('Repeat Password', validators=[InputRequired('Por favor, escribe de nuevo la contraseña')])
    submit = SubmitField('Submit')

class BriefForm(Form):
    what = StringField('What is your project about', validators=[InputRequired('Need to write a description'),
                                             Length(1, 100, 'Texto inferior a 100 caracteres')])
    who = StringField('Who is your target', validators=[DataRequired('Campo año obligatorio'),
                                              NumberRange(1850, datetime.now().year, 'Año a partir de 1850')])
    score = IntegerField('Score', validators=[DataRequired('Campo puntuacion obligatorio'),
                                              NumberRange(0, 10, 'Puntuacion entre 0 y 10')])
    submit = SubmitField('Add')

class SearchForm(Form):
    name = StringField('Name', validators=[Length(1, 100, 'Texto inferior a 100 caracteres')])
    year = IntegerField('Year', validators=[NumberRange(1850, datetime.now().year, 'Año a partir de 1850')])
    submit = SubmitField('Search')
