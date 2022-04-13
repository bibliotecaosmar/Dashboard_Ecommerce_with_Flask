from itsdangerous import URLSafeTimedSerializer
from flask import session
from app import app


def generate_confirmation_token(email):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return s.dumps(email, salt='email-confirm')

def confirm_token(token, expiration, active):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    if active:
        s.loads(token, salt='email-confirm', max_age=expiration)
        active = False   
    else:
        s.loads(token, salt='email-confirm', max_age=0)
    return active

def decode_confirmation_token(token):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return s.loads(token, salt='email-confirm')