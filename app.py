from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
from models.models import db, User
from routes.auth import auth_bp    # Blueprint para autenticación
from routes.tasks import tasks_bp  # Blueprint para tareas
from routes.oauth import oauth_bp  # Blueprint para OAuth
from dotenv import load_dotenv

# Cargar el archivo .env
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Configuración de la base de datos
    db.init_app(app)

    # Inicializar base de datos en el contexto de la app
    with app.app_context():
        db.create_all()

    # Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('tasks.dashboard'))
        return redirect(url_for('auth.login'))

    # Registrar Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(oauth_bp, url_prefix='/oauth')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
