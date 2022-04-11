from itsdangerous import URLSafeTimedSerializer
from flask import session
from app import app


def generate_recovery_token(email):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return s.dumps(email, salt='recovery-account')

def recovery_token(token, expiration=3600):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    if not password_modified:
        if active:
            email = s.loads(token, salt='recovery-account', max_age=expiration)
            active = False
        else:
            email = s.loads(token, salt='recovery-account', max_age=300)
        return email
    else:
        return s.loads(token, salt='recovery-account', max_age=0)

def decode_recovery_token(token):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return s.loads(token, salt='recovery-account')