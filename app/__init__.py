from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists

# Objeto da aplicação flask
app = Flask(__name__)

# Configurações
app.config.from_object('config')

# Define banco de dados importados em controllers
db = SQLAlchemy(app)

migrate = Migrate(app, db)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'clientes.login'

'''DATABASE-PRODUÇÃO
engine = create_engine('mysql://teste:teste1234@teste.tk/user1')
if not database_exists(engine.url):
    create_database(engine.url, encoding='utf8mb4')
'''
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# @app.errorhandler(401)
# def nao_autorizado(erro):
#     flash('É necessário está logado para acessar essa página.', 'erro')
#     return redirect(url_for('clientes.login'))

# IMPORTA TODOS OS BLUEPRINT
from app.home.controller import home
from app.clientes.controllers import clientes

app.register_blueprint(home)
app.register_blueprint(clientes)


from app.clientes import models

