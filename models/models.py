from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
    :no-index:
    Model representing a user in the application.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): The user's unique username. Required field.
        password (str): The user's password. Can be NULL for OAuth-authenticated users.
        oauth_provider (str): Name of the OAuth authentication provider (optional).
        oauth_id (str): Unique identifier provided by the OAuth service (optional).
        tasks (list[Task]): List of tasks associated with the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=True)
    oauth_provider = db.Column(db.String(50), nullable=True)
    oauth_id = db.Column(db.String(100), nullable=True)
    tasks = db.relationship('Task', backref='owner', lazy=True)


class Task(db.Model):
    """
    :no-index:
    Model representing a task in the application.

    Attributes:
        id (int): Unique identifier for the task.
        title (str): Title of the task. Required field.
        description (str): Detailed description of the task (optional).
        priority (int): Priority level of the task (e.g., 1 for low, 2 for medium, etc.).
        is_complete (bool): Indicates if the task is completed. Defaults to False.
        image (str): Path to an attached image for the task (optional).
        user_id (int): Identifier of the user to whom the task belongs.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.Integer, nullable=False)
    is_complete = db.Column(db.Boolean, default=False)
    image = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
