# Acceptance test

## 1. User Registration and Login
**Description**: Verifies that a user can register and log in successfully.

**Referenced Code**:
```python
def test_user_register_login(flask_app):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:5000/auth/register")

        page.fill("input[name='username']", "testuser")
        page.fill("input[name='password']", "password123")
        page.click("button[type='submit']")
        assert page.goto("http://localhost:5000/auth/login")

        page.fill("input[name='username']", "testuser")
        page.fill("input[name='password']", "password123")
        page.click("button[type='submit']")
        assert page.goto("http://localhost:5000/tasks/dashboard")
```

**Steps**:
1. Navigate to `http://localhost:5000/auth/register`.
2. Fill in the username and password fields with valid data.
3. Click the "Register" button.
4. Redirect to the login page at `http://localhost:5000/auth/login`.
5. Fill in the username and password fields.
6. Click the "Login" button.
7. Verify that the user is redirected to `http://localhost:5000/tasks/dashboard`.

**Expected Results**:
- The user registration is successful.
- The login page is displayed after registration.
- The user can log in and access the dashboard.

---

## 2. Task Creation and Management
**Description**: Verifies that a logged-in user can create and view tasks.

**Referenced Code**:
```python
def test_task_creation_and_management(flask_app):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Autenticarse usando la función helper
        login_user(page)

        # Crear una nueva tarea
        page.fill("input[name='title']", "Tarea de prueba")
        page.fill("textarea[name='description']", "Descripción de prueba")
        page.select_option("select[name='priority']", '1')

        page.click("button.btn.btn-primary")
        assert page.locator("text=Tarea de prueba").is_visible()

        browser.close()
```

**Steps**:
1. Log in using valid credentials.
2. Navigate to the task creation form on the dashboard
3. Fill in the following fields:
   - Title: `Tarea de prueba`
   - Description: `Descripción de prueba`
   - Priority: Select `High`.
4. Click the "Create Task" button.
5. Verify that the new task appears on the dashboard.

**Expected Results**:
- The task is created successfully.
- The new task is visible on the dashboard with the correct details.

---

## 3. Responsive Design
**Description**: Tests the application's layout and usability on different screen sizes.

**Referenced Code**:
```python
def test_responsive_design(flask_app):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        login_user(page)

        sizes = [
            {"width": 1920, "height": 1080},  # Escritorio
            {"width": 768, "height": 1024},   # Tableta
            {"width": 375, "height": 667}     # Móvil
        ]

        for size in sizes:
            page.set_viewport_size(size)
            assert page.locator("button[type='submit']").is_visible()

        browser.close()
```

**Steps**:
1. Log in using valid credentials.
2. Test the layout on the following viewport sizes:
   - Desktop: `1920x1080`
   - Tablet: `768x1024`
   - Mobile: `375x667`
3. Verify that all essential elements, such as buttons and forms, are visible and functional on each viewport.

**Expected Results**:
- The layout adapts properly to each screen size.
- Buttons and forms are accessible and functional across all viewports.

---

## 4. Cross-Browser Compatibility
**Description**: Ensures the application works as expected across different browsers.

**Referenced Code**:
```python
def test_cross_browser_compatibility(flask_app):
    browsers = ["chromium", "firefox", "webkit"]

    for browser_type in browsers:
        with sync_playwright() as p:
            browser = getattr(p, browser_type).launch(headless=True)
            page = browser.new_page()

            # Usar la función de login reutilizable
            login_user(page)

            # Confirmar acceso al dashboard
            assert page.locator("h2:has-text('Task Dashboard')").is_visible()

            browser.close()
```

**Steps**:
1. Test the application on the following browsers:
   - Chromium
   - Firefox
   - Webkit
2. Log in using valid credentials.
3. Verify access to the dashboard in each browser.

**Expected Results**:
- The application is functional on all tested browsers.
- The dashboard is accessible without issues.

---

## 5. Google OAuth Login (Optional)
**Description**: Verifies that a user can log in using Google OAuth.

**Referenced Code**:
```python
# Only execute when you have version headless=True, otherwise we cannot skip the captcha.
def test_google_oauth_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(locale="en-US")
        page = context.new_page()

        page.goto("http://localhost:5000/auth/login")
        page.screenshot(path="debug_login.png")
        page.click('a:has-text("Login with Google")')
        page.wait_for_timeout(5000)

        page.fill('input[type="email"]', "testuser.tdlapp@gmail.com")
        page.click('button:has-text("Next")')
        
        page.fill('input[type="password"]', "test_user_app")
        page.click('button:has-text("Next")')
        
        page.click('button:has-text("Continuar")')

        assert page.is_visible("h2:has-text('Task Dashboard')")

        browser.close()
```

**Steps**:
1. Navigate to `http://localhost:5000/auth/login`.
2. Click the "Login with Google" button.
3. Enter valid Google account credentials (email and password).
4. Click "Next" and complete the login process.
5. Verify that the user is redirected to the dashboard.

**Expected Results**:
- The user is successfully authenticated using Google OAuth.
- The dashboard is displayed after login.

---
