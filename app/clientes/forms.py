from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, EmailField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(message='Digite um email')])
    senha = PasswordField('senha', validators=[DataRequired(message='Digite uma senha')])
    lembrar_me = BooleanField('lembrar_me')

class RegisterForm(FlaskForm):
    nome = StringField('nome', validators=[DataRequired(message='Digite um nome')])
    email = EmailField('email', validators=[DataRequired(message='Digite um email')])
    senha = PasswordField('senha', validators=[DataRequired(message='Digite uma senha')])
    
