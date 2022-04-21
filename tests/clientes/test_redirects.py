import pytest

def test_redirect_login_sucess(auth):
    auth.logout()
    with auth.login() as response:
        assert len(response.history) == 1
        assert response.request.path == '/'