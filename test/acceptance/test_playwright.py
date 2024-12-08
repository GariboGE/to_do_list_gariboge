from playwright.sync_api import sync_playwright, Page


def login_user(page: Page):
    # Navegar a la página de login
    page.goto("http://localhost:5000/auth/login")

    # Llenar el formulario de autenticación
    page.fill("input[name='username']", "testuser")
    page.fill("input[name='password']", "password123")
    page.click("button[type='submit']")

    # Confirmar que el login fue exitoso
    if not page.locator("h2:has-text('Task Dashboard')").is_visible():
        raise Exception("Login failed. Dashboard not visible.")


def test_user_register_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
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


def test_task_creation_and_management():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
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


def test_responsive_design():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
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


def test_cross_browser_compatibility():
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

 
def test_google_oauth_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(locale="en-US")
        page = context.new_page()

        page.goto("http://localhost:5000/auth/login")
        page.click('a:has-text("Login with Google")')

        page.fill('input[type="email"]', "testuser.tdlapp@gmail.com")
        page.click('button:has-text("Next")')

        page.wait_for_selector('input[type="password"]')
        page.fill('input[type="password"]', "test_user_app")
        page.click('button:has-text("Next")')


        page.click('button:has-text("Continuar")')
        page.wait_for_selector('h2:has-text("Task Dashboard")')

        # Confirmar si el test fue exitoso
        assert page.is_visible("h2:has-text('Task Dashboard')")

        browser.close()
