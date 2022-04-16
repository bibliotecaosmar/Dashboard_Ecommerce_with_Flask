from itsdangerous import URLSafeTimedSerializer
from flask import session
from app import app


def generate_recovery_token(email):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return s.dumps(email, salt='recovery-password')

def recovery_token(token, expiration, active):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    if active:
        s.loads(token, salt='recovery-password', max_age=expiration)
    else:
        s.loads(token, salt='recovery-password', max_age=0)
    return active

def decode_recovery_token(token):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return s.loads(token, salt='recovery-password')