from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField, EmailField
from wtforms.validators import DataRequired, InputRequired, EqualTo

class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(message='Digite um email')])
    senha = PasswordField('senha', validators=[DataRequired(message='Digite uma senha')])
    lembrar_me = BooleanField('lembrar_me')

class RegisterForm(FlaskForm):
    nome = StringField('nome', validators=[DataRequired(message='Digite um nome')])
    email = EmailField('email', validators=[DataRequired(message='Digite um email')])
    #senha = PasswordField('senha', validators=[DataRequired(message='Digite uma senha')])
    senha = PasswordField('senha', validators=[InputRequired(message='Digite sua senha'), EqualTo('confirma', message='As senhas não correspondem')])
    confirma = PasswordField('confirma', validators=[DataRequired(message='Confirme sua senha')])
    
class RecoveryPasswordForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(message='Digite um email')])

class ChangePasswordForm(FlaskForm):
    senha = PasswordField('senha', validators=[InputRequired(message='Digite sua senha'), EqualTo('confirma', message='As senhas não correspondem')])
    confirma = PasswordField('confirma', validators=[DataRequired(message='Confirme sua senha')])