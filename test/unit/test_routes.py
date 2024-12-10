from conftest import *


def test_login_invalid_user(client):
    # Intento de login con credenciales inválidas
    response = client.post('/auth/login', data={'username': 'wronguser', 'password': 'wrongpass'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data


def test_register_new_user(client):
    # Registro de un nuevo usuario
    response = client.post('/auth/register', data={'username': 'newuser', 'password': 'newpass'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Account created successfully! Please log in." in response.data


def test_logout(authenticated_client):
    # Cerrar sesión de un usuario autenticado
    response = authenticated_client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data  # Redirige a la página de login
