import os


class Config:
    # Base settings
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')

    # App secrets
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback_secret_key')

    # OAuth Configuration
    OAUTH_CLIENT_ID = os.getenv('OAUTH_CLIENT_ID', None)
    OAUTH_CLIENT_SECRET = os.getenv('OAUTH_CLIENT_SECRET', None)
    OAUTH_REDIRECT_URI = os.getenv('OAUTH_REDIRECT_URI', None)

    # Optional: Raise an error if any OAuth-related environment variable is missing
    if not all([OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, OAUTH_REDIRECT_URI]):
        raise ValueError("Faltan variables de entorno requeridas para OAuth")
