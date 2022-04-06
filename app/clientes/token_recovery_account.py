from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask import flash, session, redirect, url_for
from app import app


def generate_recovery_token(email):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return s.dumps(email, salt='recovery-password')

def recovery_token(token, expiration=3600):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    if session['time_recovery_pwd'] == False:
        email = s.loads(token, salt='recovery-password', max_age=expiration)
        session['time_recovery_pwd'] = True
    else:
        email = s.loads(token, salt='recovery-password', max_age=300)
    return email