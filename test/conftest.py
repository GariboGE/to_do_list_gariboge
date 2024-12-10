from werkzeug.security import generate_password_hash
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from forms.forms import *
from models.models import User, Task

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost'

@pytest.fixture
def client():
    app = create_app()
    app.config.from_object(TestConfig)
    with app.app_context():
        db.create_all() 
        yield app.test_client()
        db.session.remove()
        db.drop_all() 


@pytest.fixture
def authenticated_client(client):
    with client.application.app_context():
        user = User(username='testuser', password=generate_password_hash('testpass'))
        db.session.add(user)
        db.session.commit()

        client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'testpass'
        })
        yield client
