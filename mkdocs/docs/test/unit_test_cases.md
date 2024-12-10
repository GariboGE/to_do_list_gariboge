# Unite test

## 1. API

### Test Case 1: Successful API Response

**Description**: Validate that `get_game_deals` correctly processes and returns a list of game deals when the API responds successfully.

**Referenced Code**:
```python
@patch('services.api_service.requests.get')
def test_get_game_deals_success(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = [
        {
            'title': 'Game 1',
            'salePrice': '19.99',
            'normalPrice': '39.99',
            'dealID': '123',
            'metacriticScore': '90',
            'dealRating': '9.5'
        },
        {
            'title': 'Game 2',
            'salePrice': '15.99',
            'normalPrice': '29.99',
            'dealID': '456',
            'metacriticScore': '88',
            'dealRating': '9.0'
        }
    ]

    mock_get.return_value = mock_response

    deals = get_game_deals()

    assert len(deals) == 2
    assert deals[0]['title'] == 'Game 1'
    assert deals[1]['title'] == 'Game 2'
```

**Steps**:
1. Mock the requests.get method to simulate a successful API response with test data.
2. Call the get_game_deals function.
3. Verify that the returned list of deals matches the mocked data.

**Expected Results**:
- `get_game_deals` returns a list containing two deals with correct titles and details.

### Test Case 2: API Request Failure

**Description**: Ensure `get_game_deals` gracefully handles API request errors by returning an empty list.

**Referenced Code**:
```python
@patch('services.api_service.requests.get')
def test_get_game_deals_error(mock_get):
    mock_get.side_effect = requests.RequestException('API failure')

    deals = get_game_deals()

    assert deals == []
```

**Steps**:
1. Mock the requests.get method to raise a RequestException.
2. Call the get_game_deals function.
3. Verify that an empty list is returned.

**Expected Results**:
- `get_game_deals` returns an empty list when the API request fails.

---

## 2. Auth

### Test Case 1: Get User by Username

**Description**: Verify that `get_user_by_username` successfully retrieves a user from the database.

**Referenced Code**:  
```python
def test_get_user_by_username(client):
    with client.application.app_context():
        # Crear y agregar un usuario a la base de datos
        user = User(username='testuser', password=generate_password_hash('1234'))
        db.session.add(user)
        db.session.commit()

        # Buscar el usuario en la base de datos
        found_user = get_user_by_username('testuser')
        assert found_user is not None
        assert found_user.username == 'testuser'

        # Intentar buscar un usuario que no existe
        not_found_user = get_user_by_username('nonexistent')
        assert not_found_user is None
```

**Steps**:  
1. Create a user in the database.  
2. Search for the user by their username using `get_user_by_username`.  
3. Verify that the user is found and their username matches.

**Expected Results**:  
- The user is retrieved from the database, and the username is correct.

---

### Test Case 2: Create User

**Description**: Ensure `create_user` correctly adds a new user to the database and handles duplicate usernames.

**Referenced Code**:  
```python
def test_create_user(client):
    with client.application.app_context():
        # Intentar crear un nuevo usuario
        created = create_user('newuser', 'password')
        assert created is True

        # Verificar que el usuario existe en la base de datos
        user = get_user_by_username('newuser')
        assert user is not None

        # Intentar crear el mismo usuario de nuevo
        created_again = create_user('newuser', 'newpass')
        assert created_again is False
```

**Steps**:  
1. Attempt to create a new user using `create_user`.  
2. Verify the user exists in the database.  
3. Attempt to create the same user again and check the response.

**Expected Results**:  
- The user is created successfully the first time.  
- Creating the same user a second time returns `False`.

---

### Test Case 3: Login with Correct Credentials

**Description**: Test that a user can log in with the correct username and password.

**Referenced Code**:  
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

**Steps**:  
1. Create a user in the database with a known username and password.  
2. Use the client to post login data to `/auth/login`.  
3. Check the response status code and verify the session contains the user's ID.

**Expected Results**:  
- Response status code is `302` (redirect).  
- The session contains the user ID.

---

### Test Case 4: Login with Incorrect Credentials

**Description**: Ensure that login with incorrect username or password does not authenticate the user.

**Referenced Code**:  
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

**Steps**:  
1. Create a user in the database.  
2. Attempt to log in using incorrect credentials with the client.  
3. Check the response status code and verify that no session user ID is present.

**Expected Results**:  
- Response status code is `200`.  
- No user session is created in the client's session data.

## 3. Forms

### Test Case 1: LoginForm - Valid Data

**Description**: Verify that the `LoginForm` is validated correctly with valid username and password data.

**Referenced Code**:  
```python
def test_login_form_valid_data(client):
    form = LoginForm(data={'username': 'testuser', 'password': 'testpassword'})
    assert form.validate() is True
```

**Steps**:  
1. Create a `LoginForm` instance with valid `username` and `password`.  
2. Call the `validate()` method on the form.

**Expected Results**:  
- The form validation returns `True`.

---

### Test Case 2: LoginForm - Missing Username

**Description**: Ensure that the `LoginForm` validation fails if the username is missing.

**Referenced Code**:  
```python
def test_login_form_missing_username(client):
    form = LoginForm(data={'username': '', 'password': 'testpassword'})
    assert form.validate() is False
    assert 'This field is required.' in form.username.errors
```

**Steps**:  
1. Create a `LoginForm` instance with an empty `username` and a valid `password`.  
2. Call the `validate()` method and check the validation errors.

**Expected Results**:  
- The form validation returns `False`.  
- The error message `'This field is required.'` is present in `form.username.errors`.

---

### Test Case 3: LoginForm - Missing Password

**Description**: Ensure that the `LoginForm` validation fails if the password is missing.

**Referenced Code**:  
```python
def test_login_form_missing_password(client):
    form = LoginForm(data={'username': 'testuser', 'password': ''})
    assert form.validate() is False
    assert 'This field is required.' in form.password.errors
```

**Steps**:  
1. Create a `LoginForm` instance with a valid `username` and an empty `password`.  
2. Call the `validate()` method and check the validation errors.

**Expected Results**:  
- The form validation returns `False`.  
- The error message `'This field is required.'` is present in `form.password.errors`.

---

### Test Case 4: RegisterForm - Valid Data

**Description**: Verify that the `RegisterForm` is validated correctly with valid username and password data.

**Referenced Code**:  
```python
def test_register_form_valid_data(client):
    form = RegisterForm(data={'username': 'newuser', 'password': 'securepassword'})
    assert form.validate() is True
```

**Steps**:  
1. Create a `RegisterForm` instance with valid `username` and `password`.  
2. Call the `validate()` method.

**Expected Results**:  
- The form validation returns `True`.

---

### Test Case 5: RegisterForm - Missing Username

**Description**: Ensure that the `RegisterForm` validation fails if the username is missing.

**Referenced Code**:  
```python
def test_register_form_missing_username(client):
    form = RegisterForm(data={'username': '', 'password': 'securepassword'})
    assert form.validate() is False
    assert 'This field is required.' in form.username.errors
```

**Steps**:  
1. Create a `RegisterForm` instance with an empty `username` and a valid `password`.  
2. Call the `validate()` method and check the validation errors.

**Expected Results**:  
- The form validation returns `False`.  
- The error message `'This field is required.'` is present in `form.username.errors`.

---

### Test Case 6: RegisterForm - Missing Password

**Description**: Ensure that the `RegisterForm` validation fails if the password is missing.

**Referenced Code**:  
```python
def test_register_form_missing_password(client):
    form = RegisterForm(data={'username': 'newuser', 'password': ''})
    assert form.validate() is False
    assert 'This field is required.' in form.password.errors
```
**Steps**:  
1. Create a `RegisterForm` instance with a valid `username` and an empty `password`.  
2. Call the `validate()` method and check the validation errors.

**Expected Results**:  
- The form validation returns `False`.  
- The error message `'This field is required.'` is present in `form.password.errors`.

---

### Test Case 7: TaskForm - Valid Data

**Description**: Verify that the `TaskForm` is validated correctly with all required data provided.

**Referenced Code**:  
```python
def test_task_form_valid_data(client):
    form = TaskForm(data={
        'title': 'New Task',
        'description': 'Testing task form validation',
        'priority': 3,
        'is_complete': False
    })
    assert form.validate() is True
```

**Steps**:  
1. Create a `TaskForm` instance with valid `title`, `description`, `priority`, and `is_complete`.  
2. Call the `validate()` method.

**Expected Results**:  
- The form validation returns `True`.

---

### Test Case 8: TaskForm - Missing Title

**Description**: Ensure that the `TaskForm` validation fails if the title is missing.

**Referenced Code**:  
```python
def test_task_form_missing_title(client):
    form = TaskForm(data={
        'title': '',
        'description': 'No title provided',
        'priority': 2,
        'is_complete': False
    })
    assert form.validate() is False
    assert 'This field is required.' in form.title.errors
```

**Steps**:  
1. Create a `TaskForm` instance with an empty `title` and other valid fields.  
2. Call the `validate()` method and check the validation errors.

**Expected Results**:  
- The form validation returns `False`.  
- The error message `'This field is required.'` is present in `form.title.errors`.


## 4. Models

### Test Case 1: Create User

**Description**: Verify that a new user instance is created with the correct username and password hashing.

**Referenced Code**:  
```python
def test_create_user():
    user = User(username='newuser', password=generate_password_hash('secret'))
    assert user.username == 'newuser'
    assert user.password.startswith('scrypt:')
```

**Steps**:  
1. Create a new `User` instance with `username` as `'newuser'` and a password.  
2. Check the `username` and ensure the `password` starts with the hashing prefix.

**Expected Results**:  
- The `username` should be `'newuser'`.  
- The `password` should start with `'scrypt:'`.

---

### Test Case 2: Task Creation

**Description**: Ensure a new task is created with the correct attributes.

**Referenced Code**:  
```python
def test_task_creation():
    task = Task(title='Clean Room', description='Clean the main room', priority=3)
    assert task.title == 'Clean Room'
    assert task.priority == 3
```

**Steps**:  
1. Create a `Task` instance with `title`, `description`, and `priority`.  
2. Verify the `title` and `priority` of the task.

**Expected Results**:  
- The `title` should be `'Clean Room'`.  
- The `priority` should be `3`.

---

### Test Case 4: Create Task

**Description**: Verify that a task instance is created with the correct title, description, and priority.

**Referenced Code**:  
```python
```

**Steps**:  
1. Create a `Task` instance with a `title`, `description`, and `priority`.  
2. Check that each of these attributes matches the expected values.

**Expected Results**:  
- The `title` should be `'Write Report'`.  
- The `description` should be `'Complete the monthly report'`.  
- The `priority` should be `2`.

---

### Test Case 5: Read Task

**Description**: Ensure that a task instance is initialized correctly with the expected attributes.

**Referenced Code**:  
```python
def test_read_task():
    task = Task(title='Read Task', description='Check details of the task', priority=1)
    assert task.title == 'Read Task'
    assert task.description == 'Check details of the task'
    assert task.priority == 1
```

**Steps**:  
1. Create a `Task` instance with `title`, `description`, and `priority`.  
2. Verify that all attributes match their expected values.

**Expected Results**:  
- The `title` should be `'Read Task'`.  
- The `description` should be `'Check details of the task'`.  
- The `priority` should be `1`.

---

### Test Case 6: Update Task

**Description**: Confirm that a task's description and priority can be updated correctly.

**Referenced Code**:  
```python
def test_update_task():
    task = Task(title='Update Task', description='Old description', priority=3)
    task.description = 'Updated description'
    task.priority = 1
    assert task.description == 'Updated description'
    assert task.priority == 1
```

**Steps**:  
1. Create a `Task` instance with initial values for `title`, `description`, and `priority`.  
2. Update the `description` and `priority` attributes.  
3. Check that the changes are correctly applied.

**Expected Results**:  
- The `description` should be updated to `'Updated description'`.  
- The `priority` should be updated to `1`.

---

### Test Case 7: Delete Task

**Description**: Ensure that a task is successfully deleted and becomes inaccessible.

**Referenced Code**:  
```python
def test_delete_task():
    task = Task(title='Delete Task', description='To be deleted', priority=2)
    del task
    try:
        task
    except NameError:
        task = None
    assert task is None
```

**Steps**:  
1. Create a `Task` instance.  
2. Delete the task and attempt to access it.

**Expected Results**:  
- The task should no longer exist.  
- An attempt to access the task should raise a `NameError`.


## 5. Password Hashing

### Test Case 1: Password Hashing

**Description**: Verify that a password is properly hashed and different from its original form.

**Referenced Code**:  
```python
def test_password_hash():
    password = "SuperSecret"
    hashed_password = generate_password_hash(password)
    assert password != hashed_password
    assert hashed_password.startswith('scrypt:')

```

**Steps**:  
1. Define a password string, e.g., `"SuperSecret"`.  
2. Use the `generate_password_hash` function to hash the password.  
3. Compare the original password with the hashed password.

**Expected Results**:  
- The original password should be different from the hashed password.  
- The hashed password should start with the hashing prefix `'scrypt:'`.

## 6. Routes

### Test Case 1: Login with Invalid User Credentials

**Description**: Verify that attempting to log in with incorrect credentials results in an error message.

**Referenced Code**:  
```python
def test_login_invalid_user(client):
    response = client.post('/auth/login', data={'username': 'wronguser', 'password': 'wrongpass'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data
```

**Steps**:  
1. Send a POST request to the `/auth/login` endpoint with `'username': 'wronguser'` and `'password': 'wrongpass'`.  
2. Follow redirects to ensure the response contains the result.

**Expected Results**:  
- The response status code should be `200`.  
- The response data should include the message "Invalid username or password".

---

### Test Case 2: Register New User

**Description**: Verify the registration process for creating a new user account.

**Referenced Code**:  
```python
def test_register_new_user(client):
    response = client.post('/auth/register', data={'username': 'newuser', 'password': 'newpass'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Account created successfully! Please log in." in response.data
```

**Steps**:  
1. Send a POST request to the `/auth/register` endpoint with `'username': 'newuser'` and `'password': 'newpass'`.  
2. Follow redirects to confirm the response.

**Expected Results**:  
- The response status code should be `200`.  
- The response data should include the message "Account created successfully! Please log in."

---

### Test Case 3: Logout Authenticated User

**Description**: Ensure that logging out redirects the authenticated user back to the login page.

**Referenced Code**:  
```python
def test_logout(authenticated_client):
    response = authenticated_client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data
```

**Steps**:  
1. Authenticate a user using an authenticated client session.  
2. Send a GET request to the `/auth/logout` endpoint.  
3. Follow redirects to confirm the user is redirected.

**Expected Results**:  
- The response status code should be `200`.  
- The response data should contain the word "Login".

## 7. Tasks

### Test Case 1: Home Page Redirect for Non-Authenticated Users

**Description**: Verify that unauthenticated users trying to access the home page are redirected to the login page.

**Referenced Code**  
```python
def test_home_not_authenticated(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.location == url_for('auth.login', _external=False)
```

**Steps**  
1. Send a GET request to `/`.  
2. Check if the response status code is `302`.  
3. Verify that the redirect location points to the login route.

**Expected Results**  
- Response status code: `302`.  
- Redirect location matches `url_for('auth.login', _external=False)`.

---

### Test Case 2: Create Task with an Invalid Form

**Description**: Ensure that submitting an incomplete task form (with an empty title) still returns a valid response without redirecting.

**Referenced Code**  
```python
def test_create_task_invalid_form(authenticated_client):
    response = authenticated_client.post('/tasks/dashboard', data={
        'title': '',  # Título vacío
        'description': 'Invalid task',
        'priority': '1'  # Prioridad incorrecta
    })

    assert response.status_code == 200
```

**Steps**  
1. Send a POST request to `/tasks/dashboard` with the following data:  
   - `'title': ''` (Empty title)  
   - `'description': 'Invalid task'`  
   - `'priority': '1'`.

**Expected Results**  
- Response status code: `200`.  
- No redirects, the page is rendered with validation errors.

---

### Test Case 3: Create Task with a Valid Form

**Description**: Confirm that a task is correctly saved in the database with valid form input.

**Referenced Code**  
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

**Steps**  
1. Send a POST request to `/tasks/dashboard` with a valid task form.  
2. Verify that the response status code is `302`.  
3. Query the database to check if the new task exists.

**Expected Results**  
- The task should be saved in the database with the correct title, description, and priority.

---

### Test Case 4: Validate and Save File (Valid Scenario)

**Description**: Ensure that valid image files are correctly processed and saved.

**Referenced Code**  
```python
def test_validate_and_save_file(authenticated_client, mocker):
    mock_file = mocker.Mock()
    mock_file.filename = "sample_image.jpg"
    mock_file.seek = mocker.Mock()
    mock_file.tell.return_value = 1 * 1024 * 1024  # 1 MB

    response = validate_and_save_file(mock_file)
    
    assert response == "sample_image.jpg"
```

**Steps**  
1. Mock an image file with a filename `sample_image.jpg`.  
2. Pass it to the `validate_and_save_file` function.

**Expected Results**  
- The function should save the image file and return the filename `"sample_image.jpg"`.

---

### Test Case 5: Create Task with Image Attachment

**Description**: Verify that a task with an image is correctly created and stored in the database.

**Referenced Code**  
```python
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
```

**Steps**  
1. Send a POST request to `/tasks/dashboard` with a title, description, priority, and an image attached.

**Expected Results**  
- Response status code: `302`.  
- The task should have the correct title and image stored in the database.

---

### Test Case 6: Create Task Without an Image

**Description**: Confirm that tasks without attached images are still correctly created and redirected.

**Referenced Code**  
```python
def test_create_task_without_image(authenticated_client):
    with authenticated_client.application.app_context():
        response = authenticated_client.post('/tasks/dashboard', data={
            'title': 'Task without Image',
            'description': 'No image attached',
            'priority': 3
        })

        assert response.status_code == 302
```

**Steps**  
1. Send a POST request to `/tasks/dashboard` with task form data excluding an image attachment.

**Expected Results**  
- Response status code: `302`.  
- Task creation should succeed with no dependency on image attachments.

---

### Test Case 7: Validate and Save File with Invalid Extension

**Description**: Ensure files with unsupported extensions (e.g., `.txt`) are rejected.

**Referenced Code**  
```python
def test_validate_and_save_file_invalid_extension(authenticated_client, mocker):
    mocker.patch('services.task_service.flash')  # Mock de flash
    mock_file = mocker.Mock()
    mock_file.filename = "mal archivo.txt"
    mock_file.seek = mocker.Mock()

    response = validate_and_save_file(mock_file)
    assert response is None
```

**Steps**  
1. Mock a file named `mal_archivo.txt`.  
2. Pass it to the `validate_and_save_file` method and check the response.

**Expected Results**  
- The function should reject the file and return `None`.

---

### Test Case 8: Validate and Save File Exceeding Size Limit

**Description**: Confirm that files larger than 5 MB are rejected.

**Referenced Code**  
```python
def test_validate_and_save_file_too_large(authenticated_client, mocker):
    mocker.patch('services.task_service.flash')  # Mock de flash
    mock_file = mocker.Mock()
    mock_file.filename = "large_file.jpg"
    mock_file.seek = mocker.Mock()
    mock_file.tell.return_value = 10 * 1024 * 1024  # 10 MB (supera el límite de 5 MB)

    response = validate_and_save_file(mock_file)
    assert response is None
```

**Steps**  
1. Mock a large image file of size 10 MB.  
2. Pass it to the `validate_and_save_file` method.

**Expected Results**  
- The method should reject the file and return `None`.

---

### Test Case 9: Delete Old Files

**Description**: Verify that old files are properly deleted from storage.

**Referenced Code**  
```python
def test_delete_old_file(authenticated_client, mocker):
    filename = "existing_file.png"
    file_path = os.path.join('static/uploads', filename)

    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('os.remove')

    delete_old_file(filename)
    os.remove.assert_called_once_with(file_path)
```

**Steps**  
1. Specify an existing file `existing_file.png`.  
2. Mock the `os.path.exists` and `os.remove` calls.  
3. Pass it to the `delete_old_file` method.

**Expected Results**  
- `os.remove` should be called with the path to the file.

---

### Test Case 10: Create Task with Images

**Description**: Verify that attaching an image to a task is processed and stored correctly.

**Referenced Code**  
```python
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
```

**Steps**  
1. Send a POST request to `/tasks/dashboard` with title, description, priority, and an attached image.

**Expected Results**  
- Response status code: `302`.  
- The new task should include the filename `"task_image.jpg"` stored in the database.
