# Welcome to my ToDoList App

[GitHub repository](https://github.com/GariboGE/to_do_list_gariboge).

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
