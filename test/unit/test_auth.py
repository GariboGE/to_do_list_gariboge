from conftest import *
from services.auth_service import get_user_by_username, create_user

def test_get_user_by_username(client):
    with client.application.app_context():
        # Crear y agregar un usuario a la base de datos
        user = User(username='testuser', password=generate_password_hash('1234'))
        db.session.add(user)
        db.session.commit()

        # Buscar el usuario en la base de datos
        found_user = get_user_by_username('testuser')
        assert found_user is not None
        assert found_user.username == 'testuser'

        # Intentar buscar un usuario que no existe
        not_found_user = get_user_by_username('nonexistent')
        assert not_found_user is None


def test_create_user(client):
    with client.application.app_context():
        # Intentar crear un nuevo usuario
        created = create_user('newuser', 'password')
        assert created is True

        # Verificar que el usuario existe en la base de datos
        user = get_user_by_username('newuser')
        assert user is not None

        # Intentar crear el mismo usuario de nuevo
        created_again = create_user('newuser', 'newpass')
        assert created_again is False


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
