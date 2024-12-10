from werkzeug.security import generate_password_hash
import pytest
from flask import url_for
from app import create_app, db
from models.models import User
from conftest import authenticated_client

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = "localhost:5000"

@pytest.fixture
def client():
    app = create_app()
    app.config.from_object(TestConfig)

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


def test_create_app(client):
    app = create_app()
    assert app is not None


def test_blueprints_registration(client):
    with client.application.app_context():
        auth_routes = url_for('auth.login', _external=False)
        task_routes = url_for('tasks.dashboard', _external=False)
        oauth_routes = url_for('oauth.oauth_login', _external=False)

        assert auth_routes == '/auth/login'
        assert task_routes == '/tasks/dashboard'
        assert oauth_routes == '/oauth/login'
