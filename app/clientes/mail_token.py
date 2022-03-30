from flask import session, url_for
from itsdangerous import URLSafeTimedSerializer, TimestampSigner, SignatureExpired, BadSignature
from app import mail
from flask_mail import Message

s = URLSafeTimedSerializer('secret')
#t = TimestampSigner('secret')

def send_email_token(email, route, title, info, salt=None):
    # token = t.sign(email)
    token = s.dumps(email, salt=salt)
    msg = Message(title, sender='matheusoliveirasv@gmail.com', recipients=[email])
    link = url_for(route, token=token, _external=True)
    msg.body = info + link
    mail.send(msg)

def reset_email_token(time_session, token, time_reset, time_default, salt=None):
    if session[time_session] == False:
        session[time_session] = True
        return s.loads(token, salt=salt, max_age=time_default)
        # return t.unsign(token, max_age=time_default)
    else:
        return s.loads(token, salt=salt, max_age=time_reset)
        # return t.unsign(token, max_age=reset_time)