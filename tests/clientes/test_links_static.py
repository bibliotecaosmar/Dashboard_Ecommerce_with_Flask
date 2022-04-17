import pytest

# Testa se links da pasta static estão funcionando
def test_link_css_home(client):
    assert b"home/home.css" in client.get("/").data

