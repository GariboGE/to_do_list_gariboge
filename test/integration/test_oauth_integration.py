import pytest
from unittest.mock import patch
from flask import url_for, session
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from app import create_app, db, User


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost'  


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.config.from_object(TestConfig)
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def test_oauth_login_redirect(test_app):
    response = test_app.get(url_for('oauth.oauth_login'))
    assert response.status_code == 302


def test_oauth_callback(test_app):
    response = test_app.get(url_for('oauth.oauth_callback'), follow_redirects=True)
    assert response.status_code == 200


@patch('services.oauth_service.oauth.google.authorize_access_token')
@patch('services.oauth_service.oauth.google.parse_id_token')
def test_oauth_callback_existing_user(mock_parse_id_token, mock_authorize_access_token, test_app):
    mock_authorize_access_token.return_value = {'access_token': 'fake-token'}
    mock_parse_id_token.return_value = {
        'email': 'existing_user@gmail.com',
        'sub': '12345'
    }

    with test_app.application.app_context():
        user = User(username='existing_user@gmail.com', oauth_provider='google', oauth_id='12345')
        db.session.add(user)
        db.session.commit()

    with test_app.session_transaction() as session:
        session['oauth_nonce'] = 'fake-nonce'

    response = test_app.get(url_for('oauth.oauth_callback'))
    assert response.status_code == 302
    assert response.location == url_for('tasks.dashboard', _external=False)



def test_oauth_callback_missing_nonce(test_app):
    response = test_app.get(url_for('oauth.oauth_callback'), follow_redirects=True)
    assert response.status_code == 200


@patch('services.oauth_service.oauth.google.authorize_access_token')
@patch('services.oauth_service.oauth.google.parse_id_token')
# Test para registrar un nuevo usuario desde OAuth
def test_oauth_callback_new_user(mock_parse_id_token, mock_authorize_access_token, test_app):
    mock_authorize_access_token.return_value = {'access_token': 'fake-token'}
    mock_parse_id_token.return_value = {'email': 'newuser@gmail.com', 'sub': '67890'}

    with test_app.session_transaction() as session:
        session['oauth_nonce'] = 'fake-nonce'

    response = test_app.get(url_for('oauth.oauth_callback'))

    assert response.status_code == 302
    assert response.location == url_for('tasks.dashboard', _external=False)


@patch('services.oauth_service.oauth.google.authorize_access_token')
@patch('services.oauth_service.oauth.google.get')
def test_oauth_callback_missing_email(mock_get, mock_authorize_access_token, test_app):
    mock_authorize_access_token.return_value = {'access_token': 'fake-token'}
    mock_get.return_value.json.return_value = {'sub': 'user-without-email'}

    with test_app.session_transaction() as session:
        session['oauth_nonce'] = 'fake-nonce'

    response = test_app.get(url_for('oauth.oauth_callback'), follow_redirects=True)
    assert response.status_code == 200
