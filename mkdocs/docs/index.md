# Welcome to my ToDoList App

Go to the app [ToDoList](https://to-do-list-gariboge.onrender.com).

## About the App

The **ToDoList App** is a web-based task management tool designed to simplify daily organization and productivity. Built with Flask, it allows users to:

- **Manage Tasks**: Add, edit, and delete tasks with ease.
- **Prioritize Tasks**: Assign priority levels to tasks (`low`, `medium`, `high`, `urgent`).
- **Attach Media**: Upload images or pdfs for enhanced task descriptions.
- **Secure Authentication**: Log in via traditional methods or OAuth.
- **Interactive Dashboard**: Displays tasks with sorting by priority and integrates game discount suggestions through CheapShark.

This app is perfect for users looking for a straightforward yet powerful task organizer.

## Technologies Used

- **Flask**: Core framework for the web application.
- **SQLAlchemy**: ORM for database interactions.
- **Jinja2**: Templating engine used for generating dynamic HTML.
- **Pytest**: Framework for testing the application.
- **OAuth**: For secure user authentication.
- **Playwright**: For end-to-end acceptance tests.
- **GitHub Actions**: For continuous integration and running tests.
- **Bootstrap**: Styling framework to ensure responsive design.

For mor information visit the [GitHub repository](https://github.com/GariboGE/to_do_list_gariboge).

## Project layout

    .github/                # Contains GitHub-specific configurations and workflows
    forms/                  
        forms.py            # Contains form classes for user interactions
    instance/               # Contains de DB for the app
    models/                 
        models.py           # Defines database models for the app
    routes/                 # Defines the workflow of the app
        auth.py             
        oauth.py
        tasks.py
    services/               # Contains all the business logic
        api_service.py
        auth_service.py
        oauth_service.py
        task_service.py
    static/                 
        css/                # Contains all the CSS stylesheets for the app
            styles.css
        uploads/            # Stores images and other media files uploaded by users 
    templates/              # The HTML files for the app
        base.html
        dashboard.html
        edit_task.html
        login.html
        register.html
    test/                   
        acceptance/         # Contains end-to-end tests
        integration/        # Contains tests to validate interactions between modules
        unit/               # Contains unit tests for individual components
        conftest.py         # Contains common test fixtures and configurations
    .gitignore
    app.py                  # The main Flask application entry point
    config.py               # Contains application configuration settings
    README.md
    requirements.txt
