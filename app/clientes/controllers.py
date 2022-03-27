from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, Markup
from werkzeug.security import check_password_hash, generate_password_hash

from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse, urljoin
from app import db

# Confirmação de email
from itsdangerous import URLSafeTimedSerializer, TimestampSigner, SignatureExpired, BadSignature
from app import mail
from flask_mail import Message

from app.clientes.forms import LoginForm, RegisterForm
from app.clientes.models import Cliente
from app.clientes.user_loader import load_user

clientes = Blueprint('clientes', __name__)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

s = URLSafeTimedSerializer('secret')
t = TimestampSigner('secret')


@clientes.route('/login', methods=['GET', 'POST'])
def login(): 
    if not current_user.is_authenticated:

        form = LoginForm()
        if form.validate_on_submit():
            cliente = Cliente.query.filter_by(email=form.email.data).first()
            
            if cliente and check_password_hash(cliente.senha, form.senha.data):

                login_user(cliente, remember=form.lembrar_me.data)
                
                if 'next' in session:
                    next = session['next']
                    if is_safe_url(next) and next is not None and next != '/logout':
                        return redirect(next)
                #flash('Bem-vindo %s' % cliente.nome)
                return redirect(url_for('home.index'))

            flash('Email ou senha incorreto.', 'erro')

        session['next'] = request.args.get('next')
        return render_template('clientes/login.html', form=form)

    return redirect(url_for('home.index'))

@clientes.route('/register', methods=['GET', 'POST'])
def register():
    if not current_user.is_authenticated:
        form = RegisterForm()

        if form.validate_on_submit():
            cliente = Cliente.query.filter_by(email=form.email.data).first()
            if cliente:
                flash(Markup('Email já cadastrado. Ir para <a href="{}">página de login.</a>'.format(url_for('clientes.login'))), 'erro')
                return redirect(url_for('clientes.register'))
    
            email = form.email.data
            token = t.sign(email)
            #token = s.dumps(email, salt='email-confirm')
            msg = Message('Confirm Email', sender='matheusoliveirasv@gmail.com', recipients=[email])
            session['time'] = False
            link = url_for('clientes.confirm_email', token=token, _external=True)
            msg.body = 'Seu link de confirmacao {}'.format(link) 
            mail.send(msg)
            flash('Um link de confirmação foi enviado para seu email. Confirme para ter acesso a sua conta.', 'email')

            # cliente = Cliente(form.nome.data, form.email.data, generate_password_hash(form.senha.data, method='sha256'), 1)
            # db.session.add(cliente)
            # db.session.commit()
            # flash('Usuário cadastrado com sucesso.', 'sucesso')
            return redirect(url_for('clientes.login'))

        return render_template('clientes/register.html', form=form)

    return redirect(url_for('home.index'))

@clientes.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        if session['time'] == False:
            email = t.unsign(token, max_age=3600)
            session['time'] = True
            #email = s.loads(token, salt='email-confirm', max_age=3600)
        else:
            email = t.unsign(token, max_age=5)
    except SignatureExpired:
        flash('Seu link de confirmação de email foi expirado.', 'erro')
        return redirect(url_for('clientes.register'))
    except BadSignature:
        flash('Link de confirmação inválido.', 'erro')
        return redirect(url_for('clientes.login'))

    flash('Seu email foi confirmado.', 'sucesso')
    return redirect(url_for('clientes.login'))
    

@clientes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))

@clientes.route('/perfil')
@login_required
def perfil():
    return render_template('clientes/perfil.html', nome=current_user.nome)

@clientes.route('/minha-conta/meus-pedidos')
@login_required
def meuspedidos():
    return 'Meus Pedidos'
