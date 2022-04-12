from itsdangerous import URLSafeTimedSerializer
from flask import session
from app import app


def generate_recovery_token(email):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return s.dumps(email, salt='recovery-account')

def recovery_token(token, active, password_modified, expiration=3600):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    if active:
        s.loads(token, salt='recovery-account', max_age=expiration)
        # parei aqui (False => True)
        return active, True
    else:
        s.loads(token, salt='recovery-account', max_age=0)
        return active, password_modified

def decode_recovery_token(token):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return s.loads(token, salt='recovery-account')