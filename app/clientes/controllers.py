from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, Markup
from werkzeug.security import check_password_hash, generate_password_hash

from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse, urljoin
from app import db

# Confirmação de email
from itsdangerous import URLSafeTimedSerializer, TimestampSigner, SignatureExpired, BadSignature
from app import mail
from flask_mail import Message

from app.clientes.forms import LoginForm, RegisterForm, RecoveryPasswordForm, ChangePasswordForm
from app.clientes.models import Cliente
from app.clientes.user_loader import load_user
from app.clientes.mail_token import send_email_token, reset_email_token

clientes = Blueprint('clientes', __name__)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


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
                url = url_for('clientes.login')
                flash(Markup(f'Email já cadastrado. Ir para <a href="{url}">página de login.</a>'), 'erro')
                return redirect(url_for('clientes.register'))
            
            session['nome'] = form.nome.data
            session['senha'] = generate_password_hash(form.senha.data, method='sha256')   
            
            send_email_token(email = form.email.data, route = 'clientes.confirm_email',
                title = 'Confirmação de email', info = 'Seu link de confirmação: ',
                salt = 'email-confirm')
            session['time_confirm_email'] = False

            flash('Um link de confirmação foi enviado para seu email. Confirme para ter acesso a sua conta.', 'email')

            return redirect(url_for('clientes.login'))

        return render_template('clientes/register.html', form=form)

    return redirect(url_for('home.index'))

@clientes.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = reset_email_token(time_session = 'time_confirm_email', token = token,
            time_reset = 5, time_default= 3600, salt = 'email-confirm')
    except SignatureExpired:
        flash('Link de confirmação de email expirado.', 'erro')
        return redirect(url_for('clientes.register'))
    except BadSignature:
        flash('Link de confirmação inválido.', 'erro')
        return redirect(url_for('clientes.login'))
    except KeyError:
        return redirect(url_for('clientes.register'))
    
    cliente = Cliente(session['nome'], email, session['senha'], False)
    db.session.add(cliente)
    db.session.commit()
    flash('Seu email foi confirmado.', 'sucesso')
    flash('Usuário cadastrado com sucesso.', 'sucesso')
    return redirect(url_for('clientes.login'))
    
@clientes.route('/recuperar_senha', methods=['GET', 'POST'])
def recuperar_senha():
    if not current_user.is_authenticated:

        form = RecoveryPasswordForm()
        
        if form.validate_on_submit():
            cliente = Cliente.query.filter_by(email=form.email.data).first()
            
            if cliente:
                send_email_token(email = form.email.data, route = 'clientes.recovery_password', 
                    title = 'Recuperação de conta', info = 'Seu link para alteração de senha: ', 
                    salt = 'recovery-password')
                session['time_recovery_pwd'] = False

                flash('Um link para alteração da sua senha foi enviado para seu email.', 'email')

                return redirect(url_for('clientes.recuperar_senha'))

            flash('Email não encontrado', 'erro')

        return render_template('clientes/recuperar_senha.html', form=form)

    return redirect(url_for('home.index'))

@clientes.route('/recovery_password/<token>', methods=['GET', 'POST'])
def recovery_password(token):
    try:
        email = reset_email_token(time_session = 'time_recovery_pwd', token = token,
            time_reset = 300, time_default= 3600, salt = 'recovery-password')
    except SignatureExpired:
        flash('Seu link de recuperação de senha foi expirado.', 'erro')
        return redirect(url_for('clientes.recuperar_senha'))
    except BadSignature:
        flash('Link de recuperação de senha inválido.', 'erro')
        return redirect(url_for('clientes.recuperar_senha'))
    except KeyError:
        return redirect(url_for('clientes.recuperar_senha'))
    
    form = ChangePasswordForm()

    cliente = Cliente.query.filter_by(email=email).first()
    if form.validate_on_submit():
        cliente.senha = generate_password_hash(form.senha.data, method='sha256')
        db.session.commit()
        flash('Sua senha foi alterada!', 'sucesso')
        return redirect(url_for('clientes.login'))
    return render_template('clientes/alterar_senha.html', email=email, form=form)

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
