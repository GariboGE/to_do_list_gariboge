from conftest import *

def test_create_user():
    user = User(username='newuser', password=generate_password_hash('secret'))
    assert user.username == 'newuser'
    assert user.password.startswith('scrypt:')
    

def test_task_creation():
    task = Task(title='Clean Room', description='Clean the main room', priority=3)
    assert task.title == 'Clean Room'
    assert task.priority == 3


def test_password_hash():
    password = "SuperSecret"
    hashed_password = generate_password_hash(password)
    assert password != hashed_password
    assert hashed_password.startswith('scrypt:')
