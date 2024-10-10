from werkzeug.security import generate_password_hash
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db
from models import User, Task


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


@pytest.fixture
def client():
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

        client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        })
        yield client


def test_login_correct_credentials(client):
    with client.application.app_context():
        user = User(username='EricG1', password=generate_password_hash('1234'))
        db.session.add(user)
        db.session.commit()

        response = client.post('/login', data={
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

        response = client.post('/login', data={
            'username': 'EricG2',
            'password': '5678'
        })
        
        assert response.status_code == 200
        with client.session_transaction() as session:
            assert '_user_id' not in session


def test_create_task_invalid(authenticated_client):
    with authenticated_client.application.app_context():
        response = authenticated_client.post('/dashboard', data={
            'title': '',
            'description': 'This is a test task',
            'priority': '1',
            'image': None
        })

        # 200 because the form only refresh the page but the task doesnt create
        assert response.status_code == 200
        task = Task.query.filter_by(description='This is a test task').first()
        assert task is None
        
def test_create_task_valid(authenticated_client):
    with authenticated_client.application.app_context():
        response = authenticated_client.get('/dashboard')
        assert response.status_code == 200 
        response = authenticated_client.post('/dashboard', data={
            'title': 'Test Task',
            'description': 'This is a test task',
            'priority': '4',
            'image': None # ANy file you wants to upload on in the test
        })

        assert response.status_code == 302
        task = Task.query.filter_by(title='Test Task').first()
        assert task is not None
        assert task.description == 'This is a test task'
        assert task.priority == 4


def test_edit_task(authenticated_client):
    with authenticated_client.application.app_context():
        user = User.query.filter_by(username='testuser').first()

        # Create a task to edit in the future
        task = Task(title='Original Task', description='Original Description', priority=1, owner=user)
        db.session.add(task)
        db.session.commit()

        # Edit the task
        response = authenticated_client.post(f'/edit_task/{task.id}', data={
            'title': 'Updated Task',
            'description': 'Updated Description',
            'priority': '2',
            'image': None
        })

        assert response.status_code == 302
        updated_task = db.session.get(Task, task.id)
        assert updated_task.title == 'Updated Task'
        assert updated_task.description == 'Updated Description'
        assert updated_task.priority == 2


def test_toggle_complete_existing_task(authenticated_client):
    with authenticated_client.application.app_context():
        user = User.query.filter_by(username='testuser').first()

        # Create a task to edit in the future
        task = Task(title='Complete Me', description='To be completed', priority=1, owner=user, is_complete=False)
        db.session.add(task)
        db.session.commit()

        # Mark the task as complete
        response = authenticated_client.post(f'/toggle_complete/{task.id}')
        assert response.status_code == 302
        updated_task = db.session.get(Task, task.id)
        assert updated_task.is_complete is True
        

def test_toggle_complete_non_existing_task(authenticated_client):
    with authenticated_client.application.app_context():
        user = User.query.filter_by(username='testuser').first()

        # Create a task to edit in the future
        task = Task(title='Complete Me', description='To be completed', priority=1, owner=user, is_complete=False)
        db.session.add(task)
        db.session.commit()

        # Find the task with a +1 to the created task is not in the DB
        response = authenticated_client.post(f'/toggle_complete/{task.id + 1}')
        assert response.status_code == 302
        updated_task = db.session.get(Task, task.id + 1)
        assert updated_task is None


if __name__ == '__main__':
    pytest.main([__file__])
