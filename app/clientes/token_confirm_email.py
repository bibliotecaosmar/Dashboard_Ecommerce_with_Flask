from itsdangerous import URLSafeTimedSerializer
from flask import session
from app import app


def generate_confirmation_token(email):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return s.dumps(email, salt='email-confirm')

def confirm_token(token, expiration, expired):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    if expired:
        email = s.loads(token, salt='email-confirm', max_age=expiration)
        expired = False   
    else:
        email = s.loads(token, salt='email-confirm', max_age=0)
    return expired

def decode_token(token):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return s.loads(token, salt='email-confirm')