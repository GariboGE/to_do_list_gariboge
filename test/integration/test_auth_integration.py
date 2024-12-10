from conftest import *


def test_login_correct_credentials(client):
    with client.application.app_context():
        user = User(username='EricG1', password=generate_password_hash('1234'))
        db.session.add(user)
        db.session.commit()

        response = client.post('/auth/login', data={
            'username': 'EricG1',
            'password': '1234'
        })

        assert response.status_code == 302

        with client.session_transaction() as session:
            assert '_user_id' in session
            assert session['_user_id'] == str(user.id)


def test_login_incorrect_credentials(client):
    with client.application.app_context():
        user = User(username='EricG2', password=generate_password_hash('1234'))
        db.session.add(user)
        db.session.commit()

        response = client.post('/auth/login', data={
            'username': 'EricG2',
            'password': '5678'
        })

        assert response.status_code == 200
        with client.session_transaction() as session:
            assert '_user_id' not in session

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