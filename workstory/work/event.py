"""
ADD_WORK:
    task_id
    date
"""
ADD_WORK = 'work:add_work'

def add_work(task_id, work_date):
    return ADD_WORK, {
        'task_id': task_id,
        'date': work_date,
    }
