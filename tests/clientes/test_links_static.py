import pytest
from pprint import pprint
from app.clientes.forms import LoginForm


# Testa se links da pasta static estão funcionando
def test_link_css_home(client):
    assert b"home/home.css" in client.get("/").data

def test_link_css_login(client):
    assert b"clientes/login-register.css" in client.get("/login").data

def test_link_css_login(client):
    assert b"clientes/login-register.css" in client.get("/register").data