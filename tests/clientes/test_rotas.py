import pytest
from pprint import pprint

def test_request_home(client):
    assert client.get("/").status_code == 200

def test_request_login(client):
    assert client.get("/login").status_code == 200

def test_request_logout(auth):
    auth.login()
    assert auth.logout().status_code == 200

def test_request_register(client):
    assert client.get("/register").status_code == 200

# def test_request_confirm_email(client):
#     ...

def test_request_recuperar_senha(client):
    assert client.get("/recuperar_senha").status_code == 200

# def test_request_recovery_account(client):
#     ...

def test_request_url_not_exists(client):
    assert client.get("/url_not_exists").status_code == 404