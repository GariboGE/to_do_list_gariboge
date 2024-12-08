import pytest
from flask import url_for
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from app import create_app, db, User

# Configuración de tu Flask test
class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost'
    

# Configuración de Flask en memoria
@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.config.from_object(TestConfig)
    with app.app_context():
        db.create_all()  # Crea base de datos temporal
        yield app.test_client()
        db.drop_all()

# Test para redireccionar al login OAuth
def test_oauth_login_redirect(test_app):
    response = test_app.get(url_for('oauth.oauth_login'))
    assert response.status_code == 302  # Redirecciona a Login OAuth

def test_oauth_callback(test_app):
    response = test_app.get(url_for('oauth.oauth_callback'), follow_redirects=True)

    # Asegurarse de que Flask redirecciona correctamente
    assert response.status_code == 200

