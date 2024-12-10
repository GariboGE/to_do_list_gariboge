from conftest import *


def test_create_user():
    user = User(username='newuser', password=generate_password_hash('secret'))
    assert user.username == 'newuser'
    assert user.password.startswith('scrypt:')
    

def test_task_creation():
    task = Task(title='Clean Room', description='Clean the main room', priority=3)
    assert task.title == 'Clean Room'
    assert task.priority == 3


def test_create_task():
    task = Task(title='Write Report', description='Complete the monthly report', priority=2)
    assert task.title == 'Write Report'
    assert task.description == 'Complete the monthly report'
    assert task.priority == 2


def test_read_task():
    task = Task(title='Read Task', description='Check details of the task', priority=1)
    assert task.title == 'Read Task'
    assert task.description == 'Check details of the task'
    assert task.priority == 1


def test_update_task():
    task = Task(title='Update Task', description='Old description', priority=3)
    task.description = 'Updated description'
    task.priority = 1
    assert task.description == 'Updated description'
    assert task.priority == 1


def test_delete_task():
    task = Task(title='Delete Task', description='To be deleted', priority=2)
    del task
    try:
        task
    except NameError:
        task = None
    assert task is None
