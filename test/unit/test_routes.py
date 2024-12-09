from conftest import *

def test_login_valid_user(client):
    # Preparamos un usuario en la base de datos
    with client.application.app_context():
        user = User(username='testuser', password=generate_password_hash('testpass'))
        db.session.add(user)
        db.session.commit()

    # Prueba de login con credenciales válidas
    response = client.post('/auth/login', data={'username': 'testuser', 'password': 'testpass'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Task Dashboard" in response.data  # Asegurarnos que redirige al dashboard


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


def test_register_existing_user(client):
    # Preparamos un usuario en la base de datos
    with client.application.app_context():
        user = User(username='existinguser', password=generate_password_hash('password'))
        db.session.add(user)
        db.session.commit()

    # Intento de registro con un nombre de usuario existente
    response = client.post('/auth/register', data={'username': 'existinguser', 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Username not available, please choose another one" in response.data


def test_logout(authenticated_client):
    # Cerrar sesión de un usuario autenticado
    response = authenticated_client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data  # Redirige a la página de login
