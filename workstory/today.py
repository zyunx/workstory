import uuid
from datetime import date, datetime

from flask import (
    Blueprint, render_template, request, redirect, url_for
)

bp = Blueprint('today', __name__, url_prefix='/')

EVENT_ADD_WORK = 'today:add_work'

@bp.route('', methods=('GET',))
def home():
    from workstory import db
    from workstory import task as task_module
    from workstory.work import repository as work_repository

    conn = db.get_db()

    cur = conn.cursor()
    cur.execute('''
                SELECT id, content, created_at, status FROM task where status = 'IN_PROGRESSING' ORDER BY created_at
                ''')
    tasks = cur.fetchall()    
    cur.close()

    in_progressing_tasks = [task_module.translate_for_view(t) for t in tasks]

    work_items = work_repository.get_works_today()
    # cur = conn.cursor()
    # cur.execute('''
    #             SELECT work_date, task_content, status FROM v_work
    #             ''')
    # work_items = cur.fetchall()    
    # cur.close()
    work_task_id_set = [w['task_id'] for w in work_items]
    in_progressing_tasks = filter(lambda t: t['id'] not in work_task_id_set, in_progressing_tasks)

    conn.commit()


    return render_template('today/home.html', 
                           tasks=tasks,
                           today=date.today().strftime('%Y-%m-%d'),
                           in_progressing_tasks=in_progressing_tasks,
                           work_items=work_items,
                           new_task_id=str(uuid.uuid4()))


@bp.route('/add_work', methods=('POST', ))
def add_work():
    from workstory import db
    from yevent import repository as event_repository
    from workstory.work import event as work_event 

    conn = db.get_db()

    task_id = request.form['task_id']
    work_date = date.today()
    
    event_id = str(uuid.uuid4())
    event_type, event_content = work_event.add_work(task_id, work_date)
    event_repository.create_event(conn, event_id, event_type, event_content)

    # cur = conn.cursor()
    # cur.execute

    # cur = conn.cursor()
    # cur.execute('''
    #             INSERT INTO work (work_date, task_id) VALUES (%s, %s)
    #             ''', (date.today(), task_id))
    # cur.close()
    conn.commit()

    return redirect(url_for('today.home'))
