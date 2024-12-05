import pytest
from app import db
from models import User, Task


@pytest.fixture
def new_user():
    """Crea un usuario de prueba para usar en los tests."""
    return User(username='testuser', password='hashedpassword')


@pytest.fixture
def new_task(new_user):
    """Crea una tarea de prueba asociada a un usuario."""
    return Task(
        title='Test Task',
        description='This is a test task',
        priority=3,
        is_complete=False,
        owner=new_user
    )


def test_user_creation(new_user):
    """Prueba que se pueda crear un usuario con los atributos esperados."""
    assert new_user.username == 'testuser'
    assert new_user.password == 'hashedpassword'


def test_user_representation(new_user):
    """Prueba la representación de cadena del usuario (si está definida)."""
    db.session.add(new_user)
    db.session.commit()
    assert str(new_user) == '<User testuser>'  # Cambia esto si tu modelo tiene otro __repr__


def test_task_creation(new_task):
    """Prueba que se pueda crear una tarea con los atributos esperados."""
    assert new_task.title == 'Test Task'
    assert new_task.description == 'This is a test task'
    assert new_task.priority == 3
    assert new_task.is_complete is False
    assert new_task.owner.username == 'testuser'


def test_task_default_is_complete(new_user):
    """Prueba que el campo `is_complete` sea False por defecto."""
    task = Task(
        title='Default Task',
        description='A task without a complete flag set',
        priority=2,
        owner=new_user
    )
    assert task.is_complete is False


def test_task_representation(new_task):
    """Prueba la representación de cadena de una tarea (si está definida)."""
    db.session.add(new_task)
    db.session.commit()
    assert str(new_task) == '<Task Test Task>'  # Cambia esto si tu modelo tiene otro __repr__


def test_task_user_relationship(new_task):
    """Prueba que una tarea esté asociada al usuario correcto."""
    db.session.add(new_task.owner)
    db.session.add(new_task)
    db.session.commit()

    retrieved_task = Task.query.first()
    assert retrieved_task.owner.username == 'testuser'


def test_user_task_relationship(new_user):
    """Prueba que un usuario pueda tener múltiples tareas."""
    task1 = Task(title='Task 1', description='First task', priority=1, owner=new_user)
    task2 = Task(title='Task 2', description='Second task', priority=2, owner=new_user)
    
    db.session.add(new_user)
    db.session.add_all([task1, task2])
    db.session.commit()

    user = User.query.first()
    assert len(user.tasks) == 2
    assert user.tasks[0].title == 'Task 1'
    assert user.tasks[1].title == 'Task 2'
