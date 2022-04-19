import pytest

def test_request_pedidos(auth):
    auth.login()
    assert auth.pedidos().status_code == 200