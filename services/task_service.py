from werkzeug.utils import secure_filename
from models.models import db, Task
from flask import flash
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
MAX_FILE_SIZE = 5 * 1024 * 1024


def allowed_file(filename):
    """
    Check if the provided file has an allowed extension.

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file has an allowed extension, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_and_save_file(file):
    """
    Validate and save an uploaded file to the server.

    This function checks if the file has an allowed extension and is within the size limit.
    If validation passes, the file is saved in the 'static/uploads' directory.

    Args:
        file (FileStorage): The uploaded file object.

    Returns:
        str: The filename if successfully saved, None otherwise.
    """
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
    """
    Delete an old file from the server storage.

    Args:
        filename (str): The name of the file to be deleted.

    Returns:
        None
    """
    if filename:
        old_file_path = os.path.join('static/uploads', filename)
        if os.path.exists(old_file_path):
            os.remove(old_file_path)


def get_tasks_by_user(user):
    """
    Retrieve all tasks belonging to a specific user, sorted by priority.

    Args:
        user (User): The user for whom tasks are being retrieved.

    Returns:
        list: A list of Task objects belonging to the specified user, sorted by priority.
    """
    return Task.query.filter_by(owner=user).order_by(Task.priority).all()


def create_task(form, user):
    """
    Create a new task and save it to the database.

    This function allows creating a task with an optional image attachment.

    Args:
        form (Form): A form object containing task details (title, description, priority, image).
        user (User): The user who owns the task.

    Returns:
        None
    """
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
    """
    Update an existing task's details.

    This function allows updating the title, description, priority, and image attachment of a task.

    Args:
        task_id (int): The ID of the task to update.
        user (User): The user attempting to update the task.
        form (Form, optional): A form object containing updated task details.

    Returns:
        Task: The updated task object, or None if the user is not the owner of the task.
    """
    task = db.session.get(Task, task_id)
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
    """
    Toggle the completion status of a task.

    This function switches the `is_complete` status of a task and commits the changes to the database.

    Args:
        task_id (int): The ID of the task to update.
        user (User): The user attempting to toggle the completion status of the task.

    Returns:
        None
    """
    task = db.session.get(Task, task_id)
    if task and task.owner == user:
        task.is_complete = not task.is_complete
        db.session.commit()
