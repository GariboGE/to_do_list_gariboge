from werkzeug.security import generate_password_hash
from models.models import db, User


def get_user_by_username(username):
    return db.session.query(User).filter_by(username=username).first()


def create_user(username, password):
    existing_user = get_user_by_username(username)
    if existing_user:
        return False
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return True
