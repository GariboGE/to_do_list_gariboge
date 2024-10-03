from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Task
from forms import LoginForm, RegisterForm, TaskForm
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))  # Cambiar aquí


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(username=form.username.data).first()  # Usar db.session.query aquí
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = TaskForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join('static/uploads', filename))
        new_task = Task(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            owner=current_user,
            image=filename
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('dashboard'))

    tasks = Task.query.filter_by(owner=current_user).order_by(Task.priority).all()
    return render_template('dashboard.html', form=form, tasks=tasks)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/edit_task/<int:task_id>', methods=['POST'])
@login_required
def edit_task(task_id):
    task = db.session.get(Task, task_id)  # Cambiar aquí
    if task and task.owner == current_user:
        # Actualiza la tarea
        task.title = request.form['title']
        task.description = request.form['description']
        task.priority = request.form['priority']
        db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/toggle_complete/<int:task_id>', methods=['POST'])
@login_required
def toggle_complete(task_id):
    task = db.session.get(Task, task_id)  # Cambiar aquí
    if task and task.owner == current_user:
        task.is_complete = not task.is_complete
        db.session.commit()
    return redirect(url_for('dashboard'))


if __name__ == "__main__":
    app.run()
