from app import mail
from flask_mail import Message


def send_email(subject, email, template):
    msg = Message(
        subject, 
        recipients=[email], 
        html=template, 
        sender='matheusoliveirasv@gmail.com'
        )
    mail.send(msg)