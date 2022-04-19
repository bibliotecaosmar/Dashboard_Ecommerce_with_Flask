import pytest
from app import create_app


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

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, email='gifebo3596@eosbuzz.com', password='1234'):
        return self._client.post(
            '/login',
            data={'email': email, 'password': password},
            follow_redirects=True
        )

    def logout(self):
        return self._client.get('/logout', follow_redirects=True)

    def profile(self):
        return self._client.get('/perfil', follow_redirects=True)

    # Rotas de minha conta
    def pedidos(self):
        return self._client.get('/pedidos', follow_redirects=True)

@pytest.fixture
def auth(client):
    return AuthActions(client)

