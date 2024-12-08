from flask import Blueprint, redirect, url_for, session, flash, current_app
from flask_login import login_user
from services.oauth_service import oauth, init_oauth
from models.models import User, db
import secrets

oauth_bp = Blueprint('oauth', __name__)

@oauth_bp.before_app_request
def setup_oauth():
    init_oauth(current_app)


@oauth_bp.route('/login')
def oauth_login():
    # Generar nonce y guardarlo en la sesión
    nonce = secrets.token_urlsafe(16)
    session['oauth_nonce'] = nonce

    redirect_uri = url_for('oauth.oauth_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri, nonce=nonce)


@oauth_bp.route('/callback')
def oauth_callback():
    try:
        # Google toke
        token = oauth.google.authorize_access_token()
        nonce = session.pop('oauth_nonce', None)
        if not nonce:
            raise Exception("Nonce perdido o no proporcionado.")

        # Validate token
        idinfo = oauth.google.parse_id_token(token, nonce=nonce)

        # Extract email
        email = idinfo.get('email')
        if not email:
            raise Exception("No se obtuvo email del proveedor.")

        # Search user or create a new one
        user = User.query.filter_by(username=email).first()
        if not user:
            user = User(username=email, oauth_provider='google', oauth_id=idinfo['sub'])
            db.session.add(user)
            db.session.commit()

        # Login
        login_user(user)
        flash('Inicio de sesión exitoso.', 'success')
        return redirect(url_for('tasks.dashboard'))

    except Exception as e:
        flash(f'Error al iniciar sesión: {str(e)}', 'danger')
        return redirect(url_for('auth.login'))
