import uuid
from datetime import date

from flask import (
    Blueprint, render_template, request, redirect, url_for
)

bp = Blueprint('today', __name__, url_prefix='/')

@bp.route('', methods=('GET',))
def home():
    from workstory import db
    from workstory import task as task_module

    conn = db.get_db()

    cur = conn.cursor()
    cur.execute('''
                SELECT id, content, created_at, status FROM task where status = 'IN_PROGRESSING' ORDER BY created_at
                ''')
    tasks = cur.fetchall()    
    cur.close()

    in_progressing_tasks = [task_module.translate_for_view(t) for t in tasks]

    cur = conn.cursor()
    cur.execute('''
                SELECT work_date, task_content, status FROM v_work
                ''')
    work_items = cur.fetchall()    
    cur.close()

    conn.commit()


    return render_template('today/home.html', 
                           tasks=tasks,
                           today=date.today().strftime('%Y-%m-%d'),
                           in_progressing_tasks=in_progressing_tasks,
                           work_items=work_items,
                           new_task_id=str(uuid.uuid4()))


@bp.route('/add_work', methods=('POST', ))
def add_work():
    task_id = request.form['task_id']

    from workstory import db
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute('''
                INSERT INTO work (work_date, task_id) VALUES (%s, %s)
                ''', (date.today(), task_id))
    cur.close()
    conn.commit()

    return redirect(url_for('today.home'))
