from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, Markup
from werkzeug.security import check_password_hash, generate_password_hash

from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse, urljoin
from app import db

# Confirmação de email
from app.clientes.token_confirm_email import generate_confirmation_token, confirm_token, decode_confirmation_token
from app.clientes.token_recovery_account import generate_recovery_token, recovery_token, decode_recovery_token
from app.clientes.send_email import send_email
from itsdangerous import SignatureExpired, BadSignature
import datetime

from app.clientes.forms import LoginForm, RegisterForm, RecoveryPasswordForm, ChangePasswordForm
from app.clientes.models import Cliente, ConfirmEmail, RecoveryAccount
from app.clientes.user_loader import load_user

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
                if cliente.confirmado:
                    login_user(cliente, remember=form.lembrar_me.data)
                    if 'next' in session:
                        next = session['next']
                        if is_safe_url(next) and next is not None and next != '/logout':
                            return redirect(next)
                    #flash('Bem-vindo %s' % cliente.nome)
                    return redirect(url_for('home.index'))

                flash('Seu email ainda não foi confirmado.', 'email')
                return redirect(url_for('clientes.login'))         
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
                if cliente.confirmado:
                    url = url_for('clientes.login')
                    flash(Markup(f'Email já cadastrado. Ir para <a href="{url}">página de login.</a>'), 'erro')
                    return redirect(url_for('clientes.register'))     
                db.session.delete(cliente)
                db.session.commit()

            nome = form.nome.data
            email = form.email.data
            senha = generate_password_hash(form.senha.data, method='sha256')

            cliente = Cliente(nome, email, senha)
            db.session.add(cliente)
            db.session.commit()

            token = generate_confirmation_token(email)
            link = url_for('clientes.confirm_email', token=token, _external=True)
            html = render_template('clientes/confirm_email.html', link=link)
            subject = 'Confirmação de email'

            # session['time_confirm_email'] = False

            confirm = ConfirmEmail(token, 3600, cliente.id)
            db.session.add(confirm)
            db.session.commit()

            send_email(subject, email, html)
           
            flash('Um link de confirmação foi enviado para seu email. Confirme para ter acesso a sua conta.', 'email')

            return redirect(url_for('clientes.login'))

        return render_template('clientes/register.html', form=form)

    return redirect(url_for('home.index'))

@clientes.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = decode_confirmation_token(token)
        cliente = Cliente.query.filter_by(email=email).first()
        confirm = ConfirmEmail.query.filter_by(cliente_id=cliente.id).first()

        expiration = confirm.expiration
        active = confirm.active
        
        active = confirm_token(token, expiration, active)
        confirm.active = active
        db.session.commit()
    except SignatureExpired:
        flash('Link de confirmação de email expirado.', 'erro')
        return redirect(url_for('clientes.register'))
    except BadSignature:
        flash('Link de confirmação inválido.', 'erro')
        return redirect(url_for('clientes.login'))
    except KeyError:
        return redirect(url_for('clientes.register'))
 
    # cliente = Cliente.query.filter_by(email=email).first()
    if cliente.confirmado:
        flash('Email já confirmado. Por favor faça o login', 'sucesso')
    else:
        cliente.confirmado = True
        cliente.data_modificacao = datetime.datetime.now()
        db.session.commit()
        flash('Seu email foi confirmado.', 'sucesso')
        flash('Cadastro concluído com sucesso.', 'sucesso')
    # flash('Usuário cadastrado com sucesso.', 'sucesso')
    return redirect(url_for('clientes.login'))
    
@clientes.route('/recuperar_conta', methods=['GET', 'POST'])
def recuperar_conta():
    if not current_user.is_authenticated:

        form = RecoveryPasswordForm()
        
        if form.validate_on_submit():
            cliente = Cliente.query.filter_by(email=form.email.data).first()
            recovery = RecoveryAccount.query.filter_by(cliente_id=cliente.id).first()

            # Reseta qualquer token de recuperação no db se existir
            if recovery:
                db.session.delete(recovery)
                db.session.commit()
            
            if cliente:
                email = form.email.data
                
                token = generate_recovery_token(email)
                link = url_for('clientes.recovery_account', token=token, _external=True)
                html = render_template('clientes/recovery_account.html', link=link)
                subject = 'Recuperação de conta'

                recovery = RecoveryAccount(cliente.id, True, False)

                db.session.add(recovery)
                db.session.commit()
                
                send_email(subject, email, html)

                flash('Um link para alteração da sua senha foi enviado para seu email.', 'email')

                return redirect(url_for('clientes.recuperar_conta'))

            flash('Email não encontrado', 'erro')

        return render_template('clientes/recuperar_conta.html', form=form)

    return redirect(url_for('home.index'))

@clientes.route('/recovery_account/<token>', methods=['GET', 'POST'])
def recovery_account(token):
    try:
        email = decode_recovery_token(token)
        cliente = Cliente.query.filter_by(email=email).first()
        recovery = RecoveryAccount.query.filter_by(cliente_id=cliente.id).first()

        active = recovery.active
        password_modified = recovery.password_modified

        active, password_modified = recovery_token(token, active, password_modified)
    except SignatureExpired:
        flash('Seu link de recuperação de conta foi expirado.', 'erro')
        return redirect(url_for('clientes.recuperar_conta'))
    except BadSignature:
        flash('Link de recuperação de conta inválido.', 'erro')
        return redirect(url_for('clientes.recuperar_conta'))
    except KeyError:
        return redirect(url_for('clientes.recuperar_conta'))
    
    form = ChangePasswordForm()


    if form.validate_on_submit():
        if recovery.active:
            # Comita apenas a tabela RecoveryAccount
            if recovery.password_modified:
                # Deleta do banco o recovery para nenhuma outra página passar aberta passar
                db.session.delete(recovery)
                db.session.commit()
                flash('Sua senha já foi alterada', 'erro')
                return redirect(url_for('clientes.login'))
            
            # Comita senha nova e RecoveryAccount
            cliente.senha = generate_password_hash(form.senha.data, method='sha256')
            recovery.password_modified = True
            db.session.commit()
            flash('Sua senha foi alterada!', 'sucesso')
            return redirect(url_for('clientes.login'))
        
        # Não comita nada
        flash('Link expirou', 'erro')
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
