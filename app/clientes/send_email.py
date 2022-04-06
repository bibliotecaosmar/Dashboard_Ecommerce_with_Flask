from app import mail
from flask_mail import Message


def send_email(title, email, msg_body):
    msg = Message(title, sender='matheusoliveirasv@gmail.com', recipients=[email])
    msg.body = msg_body 
    mail.send(msg)