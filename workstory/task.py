import uuid

from flask import (
    Blueprint, render_template, request, redirect, url_for
)

bp = Blueprint('task', __name__, url_prefix='/task')

TASK_STATUS_TODO = 'TODO'
TASK_STATUS_COMPLETE = 'COMPLETE'
TASK_STATUS_IN_PROGRESSING = 'IN_PROGRESSING'
TASK_STATUS_CANCEL = 'CANCEL'


def translate_for_view(task):
    return {
        'id': task[0],
        'content': task[1],
        'created_at': task[2].strftime('%Y-%m-%d %H:%M:%S'),
        'status': task[3],
    }

@bp.route('/', methods=('GET',))
def home():
    from . import db
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute('SELECT id, content, created_at, status FROM task')
    tasks = cur.fetchall()
    tasks = [translate_for_view(task) for task in tasks]

    in_progressing_tasks = filter(lambda t: t['status'] == TASK_STATUS_IN_PROGRESSING, tasks)
    todo_tasks = filter(lambda t: t['status'] == TASK_STATUS_TODO, tasks)
    completed_tasks = filter(lambda t: t['status'] == TASK_STATUS_COMPLETE, tasks)
    canceled_tasks = filter(lambda t: t['status'] == TASK_STATUS_CANCEL, tasks)

    
    cur.close()
    conn.commit()

    return render_template('task/home.html', 
                           tasks=tasks,
                           in_progressing_tasks=in_progressing_tasks,
                           todo_tasks=todo_tasks,
                           completed_tasks=completed_tasks,
                           canceled_tasks=canceled_tasks,
                           new_task_id=str(uuid.uuid4()))

@bp.route('/create', methods=('POST',))
def create():
    from . import db
    
    id = request.form['id']
    content = request.form['content']

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO task (id, content) VALUES (%s, %s)', (id, content))
    cur.close()
    conn.commit()

    return redirect(url_for('task.home'))

@bp.route('/<id>/set_status', methods=('POST', ))
def set_status(id):
    from . import db
    
    status = request.form['status']

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute('UPDATE task SET status = %s WHERE id = %s', (status, id))
    cur.close()
    conn.commit()

    return redirect(url_for('task.home'))
