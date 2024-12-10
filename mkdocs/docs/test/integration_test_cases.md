# Integration test

## 1. App Integration

#### Test Case: App Creation
- **Description**: Verify that the app is created successfully.
- **Referenced Code**:
```python
def test_create_app(client):
    app = create_app()
    assert app is not None
```
- **Steps**:
  1. Call the `create_app()` function.
  2. Check if the returned object is not `None`.
- **Expected Result**: The app object is created successfully.

#### Test Case: Blueprint Registration
- **Description**: Verify that all blueprints are registered correctly.
- **Referenced Code**:
```python
def test_blueprints_registration(client):
    with client.application.app_context():
        auth_routes = url_for('auth.login', _external=False)
        task_routes = url_for('tasks.dashboard', _external=False)
        oauth_routes = url_for('oauth.oauth_login', _external=False)

        assert auth_routes == '/auth/login'
        assert task_routes == '/tasks/dashboard'
        assert oauth_routes == '/oauth/login'
```
- **Steps**:
  1. Access the route for login, dashboard, and OAuth login using `url_for`.
  2. Verify the routes are correct:
     - `/auth/login`
     - `/tasks/dashboard`
     - `/oauth/login`
- **Expected Result**: All routes match their expected values.

---

## 2. Auth Integration

#### Test Case: Login with Correct Credentials
- **Description**: Verify that a user can log in with correct credentials.
- **Referenced Code**:
```python
def test_login_correct_credentials(client):
    with client.application.app_context():
        user = User(username='EricG1', password=generate_password_hash('1234'))
        db.session.add(user)
        db.session.commit()

        response = client.post('/auth/login', data={
            'username': 'EricG1',
            'password': '1234'
        })

        assert response.status_code == 302

        with client.session_transaction() as session:
            assert '_user_id' in session
            assert session['_user_id'] == str(user.id)
```
- **Steps**:
  1. Create a user in the database with username `EricG1` and password `1234`.
  2. Submit a POST request to `/auth/login` with valid credentials.
  3. Check if the response redirects to the dashboard.
- **Expected Result**: User logs in successfully and is redirected to the dashboard.

#### Test Case: Login with Incorrect Credentials
- **Description**: Verify that a user cannot log in with incorrect credentials.
- **Referenced Code**:
```python
def test_login_incorrect_credentials(client):
    with client.application.app_context():
        user = User(username='EricG2', password=generate_password_hash('1234'))
        db.session.add(user)
        db.session.commit()

        response = client.post('/auth/login', data={
            'username': 'EricG2',
            'password': '5678'
        })

        assert response.status_code == 200
        with client.session_transaction() as session:
            assert '_user_id' not in session

```
- **Steps**:
  1. Create a user in the database with username `EricG2` and password `1234`.
  2. Submit a POST request to `/auth/login` with incorrect credentials.
  3. Check the response status and session.
- **Expected Result**: Login fails and no user session is created.

#### Test Case: Register with Existing Username
- **Description**: Verify that registration fails if the username already exists.
- **Referenced Code**:
```python
def test_register_existing_user(client):
    # Preparamos un usuario en la base de datos
    with client.application.app_context():
        user = User(username='existinguser', password=generate_password_hash('password'))
        db.session.add(user)
        db.session.commit()

    # Intento de registro con un nombre de usuario existente
    response = client.post('/auth/register', data={'username': 'existinguser', 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Username not available, please choose another one" in response.data
```
- **Steps**:
  1. Create a user in the database with username `existinguser`.
  2. Attempt to register with the same username.
  3. Check the response for the error message.
- **Expected Result**: Registration fails and displays an error message.

---

## 3. OAuth Integration

#### Test Case: OAuth Login Redirect
- **Description**: Verify that the OAuth login redirects the user to the provider's login page.
- **Referenced Code**:
```python
def test_oauth_login_redirect(test_app):
    response = test_app.get(url_for('oauth.oauth_login'))
    assert response.status_code == 302
```
- **Steps**:
  1. Access the `/oauth/login` route.
  2. Check the response status code.
- **Expected Result**: Response status code is `302`.

#### Test Case: OAuth Callback for Existing User
- **Description**: Verify that an existing user is logged in after OAuth callback.
- **Referenced Code**:
```python
@patch('services.oauth_service.oauth.google.authorize_access_token')
@patch('services.oauth_service.oauth.google.parse_id_token')
def test_oauth_callback_existing_user(mock_parse_id_token, mock_authorize_access_token, test_app):
    mock_authorize_access_token.return_value = {'access_token': 'fake-token'}
    mock_parse_id_token.return_value = {
        'email': 'existing_user@gmail.com',
        'sub': '12345'
    }

    with test_app.application.app_context():
        user = User(username='existing_user@gmail.com', oauth_provider='google', oauth_id='12345')
        db.session.add(user)
        db.session.commit()

    with test_app.session_transaction() as session:
        session['oauth_nonce'] = 'fake-nonce'

    response = test_app.get(url_for('oauth.oauth_callback'))
    assert response.status_code == 302
    assert response.location == url_for('tasks.dashboard', _external=False)
```
- **Steps**:
  1. Mock OAuth provider response with an existing user’s credentials.
  2. Call the `/oauth/callback` route.
  3. Verify redirection to the dashboard.
- **Expected Result**: User is logged in and redirected to the dashboard.

#### Test Case: OAuth Callback for New User
- **Description**: Verify that a new user is registered and logged in after OAuth callback.
- **Referenced Code**:
```python
@patch('services.oauth_service.oauth.google.authorize_access_token')
@patch('services.oauth_service.oauth.google.parse_id_token')
# Test para registrar un nuevo usuario desde OAuth
def test_oauth_callback_new_user(mock_parse_id_token, mock_authorize_access_token, test_app):
    mock_authorize_access_token.return_value = {'access_token': 'fake-token'}
    mock_parse_id_token.return_value = {'email': 'newuser@gmail.com', 'sub': '67890'}

    with test_app.session_transaction() as session:
        session['oauth_nonce'] = 'fake-nonce'

    response = test_app.get(url_for('oauth.oauth_callback'))

    assert response.status_code == 302
    assert response.location == url_for('tasks.dashboard', _external=False)
```
- **Steps**:
  1. Mock OAuth provider response with new user credentials.
  2. Call the `/oauth/callback` route.
  3. Verify the user is created and redirected to the dashboard.
- **Expected Result**: New user is registered and logged in.

---

## 4. Task Integration

#### Test Case: Create Task
- **Description**: Verify that a task can be created successfully.
- **Referenced Code**:
```python
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
```
- **Steps**:
  1. Submit a POST request to `/tasks/dashboard` with task details.
  2. Check if the task is created in the database.
- **Expected Result**: Task is created with the correct details.

#### Test Case: Edit Task
- **Description**: Verify that an existing task can be edited successfully.
- **Referenced Code**:
```python
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
```
- **Steps**:
  1. Create a task in the database.
  2. Submit a POST request to `/tasks/edit_task/<task_id>` with updated details.
  3. Check the database for updated values.
- **Expected Result**: Task details are updated correctly.

#### Test Case: Toggle Task Completion
- **Description**: Verify that a task's completion status can be toggled.
- **Referenced Code**:
```python
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
```
- **Steps**:
  1. Create a task with `is_complete=False`.
  2. Submit a POST request to `/tasks/toggle_complete/<task_id>`.
  3. Check the database for updated completion status.
- **Expected Result**: Task's completion status is toggled.

#### Test Case: Retrieve Tasks by User
- **Description**: Verify that tasks are retrieved and sorted by priority.
- **Referenced Code**:
```python
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
```
- **Steps**:
  1. Create tasks with different priorities.
  2. Call the `get_tasks_by_user` function.
  3. Verify the tasks are sorted by priority.
- **Expected Result**: Tasks are sorted correctly by priority.

---