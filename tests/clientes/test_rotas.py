import pytest


def test_request_home(client):
    assert client.get("/").status_code == 200

def test_request_login(client):
    assert client.get("/login").status_code == 200

def test_request_logout(app):
    ...

def test_request_register(client):
    assert client.get("/register").status_code == 200