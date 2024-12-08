from conftest import *
import io
from services.task_service import validate_and_save_file

def test_create_task_valid(authenticated_client):
    with authenticated_client.application.app_context():
        response = authenticated_client.post('/tasks/dashboard', data={
            'title': 'Test Task',
            'description': 'Test Description',
            'priority': '4'
        })

        assert response.status_code == 302

        task = Task.query.filter_by(title='Test Task').first()
        assert task is not None
        assert task.description == 'Test Description'
        assert task.priority == 4

def test_edit_task(authenticated_client):
    with authenticated_client.application.app_context():
        user = User.query.filter_by(username='testuser').first()

        task = Task(title='Original Task', description='Edit me!', priority=1,  owner=user)
        db.session.add(task)
        db.session.commit()

        response = authenticated_client.post(f'/tasks/edit_task/{task.id}', data={
            'title': 'Updated Task',
            'description': 'Updated Description',
            'priority': '2',
            'image': None
        })

        assert response.status_code == 302

def test_toggle_complete_existing_task(authenticated_client):
    with authenticated_client.application.app_context():
        user = User.query.filter_by(username='testuser').first()

        task = Task(title='Task Toggle', description='Toggle test', priority=2, is_complete=False, owner=user)
        db.session.add(task)
        db.session.commit()

        response = authenticated_client.post(f'/tasks/toggle_complete/{task.id}')
        assert response.status_code == 302

        updated_task = db.session.get(Task, task.id)
        assert updated_task.is_complete is True


def test_validate_and_save_file(authenticated_client, mocker):
    mock_file = mocker.Mock()
    mock_file.filename = "sample_image.jpg"
    mock_file.seek = mocker.Mock()
    mock_file.tell.return_value = 1 * 1024 * 1024  # 1 MB

    response = validate_and_save_file(mock_file)
    
    assert response == "sample_image.jpg"


def test_create_task_with_image(authenticated_client):
    with authenticated_client.application.app_context():
        response = authenticated_client.post('/tasks/dashboard', data={
            'title': 'Task with Image',
            'description': 'With attached picture',
            'priority': 3,
            'image': (io.BytesIO(b"fake_data"), "file.png")
        })

        assert response.status_code == 302

        task = Task.query.filter_by(title='Task with Image').first()
        assert task is not None
        assert task.image == 'file.png'


def test_create_task_without_image(authenticated_client):
    with authenticated_client.application.app_context():
        response = authenticated_client.post('/tasks/dashboard', data={
            'title': 'Task without Image',
            'description': 'No image attached',
            'priority': 3
        })

        assert response.status_code == 302
