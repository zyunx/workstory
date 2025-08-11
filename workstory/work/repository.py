from datetime import date

def get_works_today():
    from .event import ADD_WORK

    all_events = _get_all_events()
    works = []
    for event in all_events:
        if event['event_type'] == ADD_WORK:
            print(repr(event))
            event_content = event['event_content']
            
            work_date = date.fromisoformat(event_content['date'])
            if work_date == date.today():
                task_id = event_content['task_id']
                task = _get_task(task_id)
                if task is not None:
                    work = {
                        'work_date': work_date,
                        'task_id': task_id,
                        'task_content': task['content'],
                        'status': 'TODO'
                    }
                    works.append(work)
    return works

def get_all_works():
    from .event import ADD_WORK

    all_events = _get_all_events()
    works = []
    for event in all_events:
        if event['event_type'] == ADD_WORK:
            print(repr(event))
            event_content = event['event_content']
            
            work_date = date.fromisoformat(event_content['date'])
            task_id = event_content['task_id']
            task =_get_task(task_id)
            if task is not None:
                work = {
                    'work_date': work_date,
                    'task_id': task_id,
                    'task_content': task['content'],
                    'status': 'TODO'
                }
                works.append(work)
    return works

def _get_task(task_id):
    from workstory.task import repository as task_repository
    return task_repository.get_by_id(task_id)

def _get_all_events():
    from workstory import db
    from yevent import repository as event_repository

    conn = db.get_db()
    return event_repository.get_all_events(conn)
