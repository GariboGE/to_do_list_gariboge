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
        db.create_all()  # Crear la base de datos en memoria
        yield app.test_client()
        db.session.remove()
        db.drop_all()  # Limpiar la base de datos después de las pruebas


@pytest.fixture
def authenticated_client(client):
    with client.application.app_context():
        # Crea un nuevo usuario
        user = User(username='testuser', password=generate_password_hash('testpass'))
        db.session.add(user)
        db.session.commit()  # Asegúrate de guardar el usuario en la base de datos

        # Inicia sesión con el usuario creado
        client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        })
        yield client  # Asegúrate de que el cliente autenticado se devuelve


def test_create_task(authenticated_client):
    with authenticated_client.application.app_context():
        # Verifica si el usuario está autenticado
        response = authenticated_client.get('/dashboard')
        assert response.status_code == 200  # Debe ser 200 si el usuario está autenticado
        response = authenticated_client.post('/dashboard', data={
            'title': 'TestTask',
            'description': 'ThisIsATestTask',
            'priority': '4',
            'image': None # ANy file you wants to upload on in the test
        })

        assert response.status_code == 302  # Redirecciona después de crear
        task = Task.query.filter_by(title='Test Task').first()
        assert task is not None
        assert task.description == 'This is a test task'
        assert task.priority == 1  # Asegúrate de que el tipo sea correcto


def test_edit_task(authenticated_client):
    with authenticated_client.application.app_context():
        # Obtener el usuario autenticado
        user = User.query.filter_by(username='testuser').first()

        # Primero, crea una tarea
        task = Task(title='Original Task', description='Original Description', priority=1, owner=user)
        db.session.add(task)
        db.session.commit()

        # Ahora edita la tarea
        response = authenticated_client.post(f'/edit_task/{task.id}', data={
            'title': 'Updated Task',
            'description': 'Updated Description',
            'priority': '2',
            'image': None
        })

        assert response.status_code == 302  # Redirecciona después de editar
        updated_task = db.session.get(Task, task.id)
        assert updated_task.title == 'Updated Task'
        assert updated_task.description == 'Updated Description'
        assert updated_task.priority == 2


def test_toggle_complete(authenticated_client):
    with authenticated_client.application.app_context():
        # Obtener el usuario autenticado
        user = User.query.filter_by(username='testuser').first()

        # Primero, crea una tarea
        task = Task(title='Complete Me', description='To be completed', priority=1, owner=user, is_complete=False)
        db.session.add(task)
        db.session.commit()

        # Ahora marca la tarea como completada
        response = authenticated_client.post(f'/toggle_complete/{task.id}')
        assert response.status_code == 302  # Redirecciona después de marcar como completada
        updated_task = db.session.get(Task, task.id)
        assert updated_task.is_complete is True  # Asegúrate de que la tarea ahora esté marcada como completada


if __name__ == '__main__':
    pytest.main([__file__])
