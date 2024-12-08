from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import login_required, current_user
from forms.forms import TaskForm
from services.task_service import get_tasks_by_user, create_task, update_task, toggle_task_completion
from services.api_service import get_game_deals

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/')
@login_required
def home():
    if current_user.is_authenticated:
        return redirect(url_for('tasks.dashboard'))
    else:
        return redirect(url_for('auth.login'))


@tasks_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = TaskForm()
    if form.validate_on_submit():
        create_task(form, current_user)
        return redirect(url_for('tasks.dashboard'))

    tasks = get_tasks_by_user(current_user)
    game_deals = get_game_deals()
    return render_template('dashboard.html', form=form, tasks=tasks, game_deals=game_deals)


@tasks_bp.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = update_task(task_id, current_user)
    if not task:
        abort(403)

    form = TaskForm(obj=task)
    if form.validate_on_submit():
        update_task(task_id, current_user, form)
        return redirect(url_for('tasks.dashboard'))
    return render_template('edit_task.html', form=form, task=task)


@tasks_bp.route('/toggle_complete/<int:task_id>', methods=['POST'])
@login_required
def toggle_complete(task_id):
    toggle_task_completion(task_id, current_user)
    return redirect(url_for('tasks.dashboard'))
