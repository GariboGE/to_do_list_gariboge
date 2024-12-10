# GitHub Actions Workflow Documentation

```yml
name: To Do List Tests

on:
  push:
    branches:
      - dev

jobs:
  run-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.12.5', '3.12.4', '3.12.3']

    env:
      OAUTH_CLIENT_ID: ${{ secrets.OAUTH_CLIENT_ID }}
      OAUTH_CLIENT_SECRET: ${{ secrets.OAUTH_CLIENT_SECRET }}
      OAUTH_REDIRECT_URI: http://localhost:5000/oauth/auth/callback

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest --ignore=test/acceptance --cov=app --cov=services/ --cov=routes/ --cov=forms/ --cov=models/ --cov-report=html --cov-report=term-missing
```


## Workflow Name
**To Do List Tests**

## Trigger
The workflow runs automatically on a push to the `dev` branch.

## Job: `run-tests`
This job performs the following tasks:
1. Checks out the repository code.
2. Sets up Python using multiple versions to ensure compatibility.
3. Installs required dependencies.
4. Runs the tests and generates coverage reports.

### Matrix Strategy
The job runs on the following Python versions:
- Python 3.12.5
- Python 3.12.4
- Python 3.12.3

### Environment Variables
The workflow uses the following environment variables:
- **OAUTH_CLIENT_ID**: Retrieved from GitHub Secrets.
- **OAUTH_CLIENT_SECRET**: Retrieved from GitHub Secrets.
- **OAUTH_REDIRECT_URI**: Hardcoded as `http://localhost:5000/oauth/auth/callback`.

### Steps
1. **Checkout Code**:
   - Uses the `actions/checkout@v3` action to fetch the repository.
2. **Set up Python**:
   - Configures Python based on the matrix-defined versions using `actions/setup-python@v4`.
3. **Install Dependencies**:
   - Upgrades `pip` and installs required dependencies from `requirements.txt`.
4. **Run Tests**:
   - Executes `pytest`, excluding acceptance tests.
   - Generates coverage reports in both HTML and terminal formats.
