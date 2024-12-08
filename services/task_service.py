from werkzeug.utils import secure_filename
from models.models import db, Task
from flask import abort, flash
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
MAX_FILE_SIZE = 5 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_and_save_file(file):
    if not allowed_file(file.filename):
        flash("Archivo no permitido. Sólo se aceptan imágenes.", "error")
        return None
    
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    if file_length > MAX_FILE_SIZE:
        flash(f"El archivo es demasiado grande. Límite: {MAX_FILE_SIZE // (1024 * 1024)} MB.", "error")
        return None
    
    file.seek(0)
    filename = secure_filename(file.filename)
    file.save(os.path.join('static/uploads', filename))
    return filename

def delete_old_file(filename):
    if filename:
        old_file_path = os.path.join('static/uploads', filename)
        if os.path.exists(old_file_path):
            os.remove(old_file_path)

def get_tasks_by_user(user):
    return Task.query.filter_by(owner=user).order_by(Task.priority).all()

def create_task(form, user):
    filename = None
    if form.image.data:
        filename = validate_and_save_file(form.image.data)

    new_task = Task(
        title=form.title.data,
        description=form.description.data,
        priority=form.priority.data,
        owner=user,
        image=filename
    )
    db.session.add(new_task)
    db.session.commit()

def update_task(task_id, user, form=None):
    task = Task.query.get_or_404(task_id)
    if task.owner != user:
        return None

    if form:
        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data

        if form.image.data:
            new_filename = validate_and_save_file(form.image.data)
            delete_old_file(task.image)
            task.image = new_filename
        
        db.session.commit()
    return task

def toggle_task_completion(task_id, user):
    task = Task.query.get(task_id)
    if task and task.owner == user:
        task.is_complete = not task.is_complete
        db.session.commit()