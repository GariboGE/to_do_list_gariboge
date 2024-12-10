from conftest import *
from services.task_service import validate_and_save_file, delete_old_file, get_tasks_by_user


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

        task = Task(title='Original Task', description='Edit me!', priority=1, owner=user)
        db.session.add(task)
        db.session.commit()

        response = authenticated_client.post(f'/tasks/edit_task/{task.id}', data={
            'title': 'Updated Task',
            'description': 'Updated Description',
            'priority': '2',
            'image': None
        })

        assert response.status_code == 302
        

def test_edit_task_no_image(authenticated_client):
    with authenticated_client.application.app_context():
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