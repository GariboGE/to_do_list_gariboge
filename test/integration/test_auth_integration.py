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
