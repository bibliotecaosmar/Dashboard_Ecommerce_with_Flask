from flask import Flask, render_template, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists


def create_app():
    # Objeto da aplicação flask
    app = Flask(__name__)

    # Configurações
    app.config.from_object('config')

    # Define banco de dados importados em controllers
    # db = SQLAlchemy(app)
    from app.model import db
    db.init_app(app)

    migrate = Migrate(app, db)

    from app.login_manager import lm
    lm.init_app(app)
    lm.login_view = 'clientes.login'

    csrf = CSRFProtect(app)

    # DATABASE-PRODUÇÃO
    # engine = create_engine('mysql://teste:teste1234@teste.tk/user1')
    # if not database_exists(engine.url):
    #     create_database(engine.url, encoding='utf8mb4')

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    # IMPORTA TODOS OS BLUEPRINT
    from app.home.controller import home
    from app.clientes.controllers import clientes

    app.register_blueprint(home)
    app.register_blueprint(clientes)


    from app.clientes import models

    return app

