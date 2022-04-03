from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask import flash, session, redirect, url_for
from app import app


def generate_confirmation_token(email):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return s.dumps(email, salt='email-confirm')

def confirm_token(token, expiration=3600):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    if session['time_confirm_email'] == False:
        email = s.loads(token, salt='email-confirm', max_age=expiration)
        session['time_confirm_email'] = True    
    else:
        email = s.loads(token, salt='email-confirm', max_age=0)
    return email
