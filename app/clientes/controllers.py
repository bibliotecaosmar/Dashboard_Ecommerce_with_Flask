from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse, urljoin
from app.model import db

from app.clientes.forms import LoginForm, RegisterForm
from app.clientes.models import Cliente
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
                flash('Email já cadastrado', 'erro')
                return redirect(url_for('clientes.register'))

            cliente = Cliente(form.nome.data, form.email.data, generate_password_hash(form.senha.data, method='sha256'), 1)

            db.session.add(cliente)
            db.session.commit()
            flash('Usuário cadastrado com sucesso.', 'sucesso')
            return redirect(url_for('clientes.login'))

        return render_template('clientes/register.html', form=form)

    return redirect(url_for('home.index'))

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
