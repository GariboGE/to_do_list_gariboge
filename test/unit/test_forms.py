from conftest import *

# Test para LoginForm
def test_login_form_valid_data(client):
    form = LoginForm(data={'username': 'testuser', 'password': 'testpassword'})
    assert form.validate() is True

def test_login_form_missing_username(client):
    form = LoginForm(data={'username': '', 'password': 'testpassword'})
    assert form.validate() is False
    assert 'This field is required.' in form.username.errors

def test_login_form_missing_password(client):
    form = LoginForm(data={'username': 'testuser', 'password': ''})
    assert form.validate() is False
    assert 'This field is required.' in form.password.errors

# Test para RegisterForm
def test_register_form_valid_data(client):
    form = RegisterForm(data={'username': 'newuser', 'password': 'securepassword'})
    assert form.validate() is True

def test_register_form_missing_username(client):
    form = RegisterForm(data={'username': '', 'password': 'securepassword'})
    assert form.validate() is False
    assert 'This field is required.' in form.username.errors

def test_register_form_missing_password(client):
    form = RegisterForm(data={'username': 'newuser', 'password': ''})
    assert form.validate() is False
    assert 'This field is required.' in form.password.errors

# Test para TaskForm
def test_task_form_valid_data(client):
    form = TaskForm(data={
        'title': 'New Task',
        'description': 'Testing task form validation',
        'priority': 3,
        'is_complete': False
    })
    assert form.validate() is True

def test_task_form_missing_title(client):
    form = TaskForm(data={
        'title': '',
        'description': 'No title provided',
        'priority': 2,
        'is_complete': False
    })
    assert form.validate() is False
    assert 'This field is required.' in form.title.errors
