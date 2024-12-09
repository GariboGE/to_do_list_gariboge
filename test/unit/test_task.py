from conftest import *
import io
from flask import url_for
from services.task_service import validate_and_save_file, delete_old_file, get_tasks_by_user

def test_home_not_authenticated(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.location == url_for('auth.login', _external=False)
    
'''
def test_edit_nonexistent_task(authenticated_client):
    response = authenticated_client.post('/tasks/edit_task/999')
    assert response.status_code == 500


def test_toggle_complete_nonexistent_task(authenticated_client):
    response = authenticated_client.post('/tasks/toggle_complete/999')
    assert response.status_code == 404
'''

def test_create_task_invalid_form(authenticated_client):
    response = authenticated_client.post('/tasks/dashboard', data={
        'title': '',  # Título vacío
        'description': 'Invalid task',
        'priority': '1'  # Prioridad incorrecta
    })

    assert response.status_code == 200


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


def test_validate_and_save_file_invalid_extension(authenticated_client, mocker):
    mocker.patch('services.task_service.flash')  # Mock de flash
    mock_file = mocker.Mock()
    mock_file.filename = "mal archivo.txt"
    mock_file.seek = mocker.Mock()

    response = validate_and_save_file(mock_file)
    assert response is None


def test_validate_and_save_file_too_large(authenticated_client, mocker):
    mocker.patch('services.task_service.flash')  # Mock de flash
    mock_file = mocker.Mock()
    mock_file.filename = "large_file.jpg"
    mock_file.seek = mocker.Mock()
    mock_file.tell.return_value = 10 * 1024 * 1024  # 10 MB (supera el límite de 5 MB)

    response = validate_and_save_file(mock_file)
    assert response is None



def test_delete_old_file(authenticated_client, mocker):
    filename = "existing_file.png"
    file_path = os.path.join('static/uploads', filename)

    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('os.remove')

    delete_old_file(filename)
    os.remove.assert_called_once_with(file_path)


def test_get_tasks_by_user(authenticated_client):
    with authenticated_client.application.app_context():
        user = User.query.filter_by(username='testuser').first()

        task_high = Task(title='Urgente', priority=1, owner=user)
        task_low = Task(title='Baja', priority=4, owner=user)

        db.session.add_all([task_high, task_low])
        db.session.commit()

        tasks = get_tasks_by_user(user)

        assert tasks[0].priority == 1
        assert tasks[1].priority == 4


def test_create_task_with_image(authenticated_client):
    response = authenticated_client.post('/tasks/dashboard', data={
        'title': 'Task Image Test',
        'description': 'Con imagen',
        'priority': 3,
        'image': (io.BytesIO(b"fake_data"), "task_image.jpg")
    })

    assert response.status_code == 302
    task = Task.query.filter_by(title='Task Image Test').first()
    assert task is not None
    assert task.image == 'task_image.jpg'

def test_create_task_without_image(authenticated_client):
    response = authenticated_client.post('/tasks/dashboard', data={
        'title': 'Task No Image',
        'description': 'Sin imagen',
        'priority': 2
    })

    assert response.status_code == 302


def test_update_task(authenticated_client):
    user = User.query.filter_by(username='testuser').first()

    task = Task(title='Initial Task', description='Original', priority=2, owner=user)
    db.session.add(task)
    db.session.commit()

    response = authenticated_client.post(f'/tasks/edit_task/{task.id}', data={
        'title': 'Updated Task',
        'description': 'Updated Description',
        'priority': 3
    })

    assert response.status_code == 302
    
    updated_task = db.session.get(Task, task.id)
    assert updated_task.title == 'Updated Task'
    assert updated_task.description == 'Updated Description'


def test_toggle_task_completion(authenticated_client):
    with authenticated_client.application.app_context():
        user = User.query.filter_by(username='testuser').first()

        # Crea y añade una tarea a la base de datos.
        task = Task(title='Toggle Test', description='Incompleto', owner=user, priority=1, is_complete=False)
        db.session.add(task)
        db.session.commit()

        response = authenticated_client.post(f'/tasks/toggle_complete/{task.id}')
        assert response.status_code == 302

        updated_task = db.session.get(Task, task.id)
        assert updated_task.is_complete is True

