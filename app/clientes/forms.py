from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, EmailField, HiddenField
from wtforms.validators import DataRequired, InputRequired, EqualTo

class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(message='Digite um email')])
    senha = PasswordField('senha', validators=[DataRequired(message='Digite uma senha')])
    lembrar_me = BooleanField('lembrar_me')

class RegisterForm(FlaskForm):
    nome = StringField('nome', validators=[DataRequired(message='Digite um nome')])
    email = EmailField('email', validators=[DataRequired(message='Digite um email')])
    senha = PasswordField('senha', validators=[DataRequired(message='Digite uma senha')])
    
class RecoveryPasswordForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(message='Digite um email')])

class ChangePasswordForm(FlaskForm):
    senha = PasswordField('senha', validators=[InputRequired(), EqualTo('confirma', message='Digite sua nova senha')])
    confirma = PasswordField('confirma', validators=[DataRequired(message='Confirme sua senha')])