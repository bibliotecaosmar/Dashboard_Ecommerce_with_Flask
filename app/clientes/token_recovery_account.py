from itsdangerous import URLSafeTimedSerializer
from flask import session


def generate_recovery_token(email):
    s = URLSafeTimedSerializer('SECRET_KEY')
    return s.dumps(email, salt='recovery-password')

def recovery_token(token, expiration=3600):
    s = URLSafeTimedSerializer('SECRET_KEY')
    if session['time_recovery_pwd'] == False:
        email = s.loads(token, salt='recovery-password', max_age=expiration)
        session['time_recovery_pwd'] = True
    else:
        email = s.loads(token, salt='recovery-password', max_age=300)
    return email