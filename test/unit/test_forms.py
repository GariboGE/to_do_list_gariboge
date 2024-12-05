import pytest
from wtforms import ValidationError
from forms import LoginForm, TaskForm


@pytest.fixture
def valid_login_data():
    return {'username': 'testuser', 'password': 'testpass'}


@pytest.fixture
def valid_task_data():
    """Datos válidos para probar el formulario de tareas."""
    return {
        'title': 'Test Task',
        'description': 'This is a test task',
        'priority': '3'
    }


def test_login_form_valid_data(valid_login_data):
    """Prueba que el formulario de inicio de sesión sea válido con datos correctos."""
    form = LoginForm(data=valid_login_data)
    assert form.validate() is True


def test_login_form_missing_username():
    """Prueba que el formulario de inicio de sesión sea inválido si falta el nombre de usuario."""
    form = LoginForm(data={'password': 'testpass'})
    assert form.validate() is False
    assert 'username' in form.errors


def test_login_form_missing_password():
    """Prueba que el formulario de inicio de sesión sea inválido si falta la contraseña."""
    form = LoginForm(data={'username': 'testuser'})
    assert form.validate() is False
    assert 'password' in form.errors


def test_task_form_valid_data(valid_task_data):
    """Prueba que el formulario de tareas sea válido con datos correctos."""
    form = TaskForm(data=valid_task_data)
    assert form.validate() is True


def test_task_form_missing_title():
    """Prueba que el formulario de tareas sea inválido si falta el título."""
    data = {
        'description': 'This is a test task',
        'priority': '2'
    }
    form = TaskForm(data=data)
    assert form.validate() is False
    assert 'title' in form.errors


def test_task_form_invalid_priority():
    """Prueba que el formulario de tareas sea inválido si la prioridad no es válida."""
    data = {
        'title': 'Test Task',
        'description': 'This is a test task',
        'priority': 'invalid_priority'
    }
    form = TaskForm(data=data)
    assert form.validate() is False
    assert 'priority' in form.errors


def test_task_form_optional_image(valid_task_data):
    """Prueba que el formulario de tareas sea válido sin adjuntar una imagen."""
    form = TaskForm(data=valid_task_data)
    assert form.validate() is True


def test_task_form_empty_data():
    """Prueba que el formulario de tareas sea inválido con datos vacíos."""
    form = TaskForm(data={})
    assert form.validate() is False
    assert 'title' in form.errors
    assert 'description' in form.errors
    assert 'priority' in form.errors
