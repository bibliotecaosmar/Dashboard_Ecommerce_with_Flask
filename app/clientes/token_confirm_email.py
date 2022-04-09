from itsdangerous import URLSafeTimedSerializer
from flask import session

def generate_confirmation_token(email):
    s = URLSafeTimedSerializer('SECRET KEY')
    return s.dumps(email, salt='email-confirm')

def confirm_token(token, expiration=3600):
    s = URLSafeTimedSerializer('SECRET_KEY')
    if session['time_confirm_email'] == False:
        email = s.loads(token, salt='email-confirm', max_age=expiration)
        session['time_confirm_email'] = True    
    else:
        email = s.loads(token, salt='email-confirm', max_age=0)
    return email