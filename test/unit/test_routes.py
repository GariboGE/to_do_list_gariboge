import pytest
from app import db
from werkzeug.security import generate_password_hash
from models import User, Task

@pytest.fixture
def create_test_user(client):
    """Fixture para crear un usuario de prueba."""
    with client.application.app_context():
        user = User(username='testuser', password=generate_password_hash('testpass'))
        db.session.add(user)
        db.session.commit()
        return user


def test_home_page(client):
    """Prueba que la página de inicio cargue correctamente."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the To-Do List App" in response.data


def test_dashboard_authenticated(authenticated_client):
    """Prueba que el usuario autenticado pueda acceder al dashboard."""
    response = authenticated_client.get('/dashboard')
    assert response.status_code == 200
    assert b"Your Tasks" in response.data


def test_dashboard_unauthenticated(client):
    """Prueba que un usuario no autenticado sea redirigido al iniciar sesión."""
    response = client.get('/dashboard')
    assert response.status_code == 302  # Redirección a /login
    assert "/login" in response.headers['Location']


def test_create_task_authenticated(authenticated_client):
    """Prueba que un usuario autenticado pueda crear una tarea."""
    response = authenticated_client.post('/dashboard', data={
        'title': 'New Task',
        'description': 'Task description',
        'priority': '2',
        'image': None
    })
    assert response.status_code == 302  # Redirección tras crear la tarea

    with authenticated_client.application.app_context():
        task = Task.query.filter_by(title='New Task').first()
        assert task is not None
        assert task.description == 'Task description'


def test_create_task_unauthenticated(client):
    """Prueba que un usuario no autenticado no pueda crear una tarea."""
    response = client.post('/dashboard', data={
        'title': 'New Task',
        'description': 'Task description',
        'priority': '2'
    })
    assert response.status_code == 302  # Redirección a /login
    assert "/login" in response.headers['Location']


def test_edit_task(authenticated_client):
    """Prueba que un usuario autenticado pueda editar una tarea existente."""
    with authenticated_client.application.app_context():
        user = User.query.filter_by(username='testuser').first()
        task = Task(title='Original Task', description='Original Description', priority=3, owner=user)
        db.session.add(task)
        db.session.commit()

        response = authenticated_client.post(f'/edit_task/{task.id}', data={
            'title': 'Updated Task',
            'description': 'Updated Description',
            'priority': '1'
        })

        assert response.status_code == 302  # Redirección tras editar
        updated_task = Task.query.get(task.id)
        assert updated_task.title == 'Updated Task'
        assert updated_task.description == 'Updated Description'
        assert updated_task.priority == 1


def test_toggle_complete(authenticated_client):
    """Prueba que un usuario autenticado pueda marcar una tarea como completada."""
    with authenticated_client.application.app_context():
        user = User.query.filter_by(username='testuser').first()
        task = Task(title='Task to Complete', description='Description', priority=2, owner=user, is_complete=False)
        db.session.add(task)
        db.session.commit()

        response = authenticated_client.post(f'/toggle_complete/{task.id}')
        assert response.status_code == 302  # Redirección tras cambiar el estado

        updated_task = Task.query.get(task.id)
        assert updated_task.is_complete is True


def test_delete_task(authenticated_client):
    """Prueba que un usuario autenticado pueda eliminar una tarea."""
    with authenticated_client.application.app_context():
        user = User.query.filter_by(username='testuser').first()
        task = Task(title='Task to Delete', description='Description', priority=2, owner=user)
        db.session.add(task)
        db.session.commit()

        response = authenticated_client.post(f'/delete_task/{task.id}')
        assert response.status_code == 302  # Redirección tras eliminar

        deleted_task = Task.query.get(task.id)
        assert deleted_task is None


def test_access_protected_routes_unauthenticated(client):
    """Prueba que las rutas protegidas redirijan a usuarios no autenticados."""
    protected_routes = ['/dashboard', '/edit_task/1', '/toggle_complete/1', '/delete_task/1']
    for route in protected_routes:
        response = client.get(route)
        assert response.status_code == 302
        assert "/login" in response.headers['Location']
