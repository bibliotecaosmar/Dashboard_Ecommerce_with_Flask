import pytest

def create_app():
    from flask import Flask

    app = Flask(__name__)
    app.config.from_object('config')

    from app.home.controller import home
    from app.clientes.controllers import clientes

    app.register_blueprint(home)
    app.register_blueprint(clientes)

    return app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here
    from app.clientes import models

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
