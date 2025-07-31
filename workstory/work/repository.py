from datetime import date

def get_works_today():
    from workstory import db
    from workstory.task import repository as task_repository
    from yevent import repository as event_repository
    from .event import ADD_WORK

    conn = db.get_db()
    all_events = event_repository.get_all_events(conn)
    works = []
    for event in all_events:
        if event['event_type'] == ADD_WORK:
            print(repr(event))
            event_content = event['event_content']
            
            work_date = date.fromisoformat(event_content['date'])
            if work_date == date.today():
                task_id = event_content['task_id']
                task = task_repository.get_by_id(task_id)
                if task is not None:
                    work = {
                        'work_date': work_date,
                        'task_id': task_id,
                        'task_content': task['content'],
                        'status': 'TODO'
                    }
                    works.append(work)
    return works
