from authlib.integrations.flask_client import OAuth
import os

# Crear instancia global de OAuth
oauth = OAuth()


def init_oauth(app):
    """
    Initialize and configure OAuth integration with the Flask application.

    This function sets up the OAuth client for the Flask application and registers
    the Google OAuth provider using environment variables for client ID and client secret.
    It connects the OAuth client with the Flask app and specifies the necessary endpoints.

    Args:
        app (Flask): The Flask application instance to which OAuth is attached.

    Returns:
        None
    """
    oauth.init_app(app)  # Conecta OAuth con la app Flask

    # Configuración del proveedor Google OAuth
    oauth.register(
        name='google',
        client_id=os.getenv('OAUTH_CLIENT_ID'),
        client_secret=os.getenv('OAUTH_CLIENT_SECRET'),
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
        jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
        client_kwargs={
            'scope': 'openid email profile'
    }
)
