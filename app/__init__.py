from flask import Flask, render_template, redirect, url_for, flash
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists

from app.home.controller import home
from app.clientes.controllers import clientes


def create_app():
    from app.database import db
    from app.login_manager import lm
    from app.mail import mail

    
    # Objeto da aplicação flask
    app = Flask(__name__)

    # Configurações
    app.config.from_object('config')

    # Define banco de dados importados em controllers
    db.init_app(app)

    migrate = Migrate(app, db)

    lm.init_app(app)
    lm.login_view = 'clientes.login'

    mail.init_app(app)

    # csrf = CSRFProtect(app)

    # DATABASE-PRODUÇÃO
    # engine = create_engine('mysql://teste:teste1234@teste.tk/user1')
    # if not database_exists(engine.url):
    #     create_database(engine.url, encoding='utf8mb4')

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    # IMPORTA TODOS OS BLUEPRINT
    app.register_blueprint(home)
    app.register_blueprint(clientes)

    from app.clientes import models

    return app

