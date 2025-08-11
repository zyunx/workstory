import uuid
from datetime import date, datetime
import itertools

from flask import (
    Blueprint, render_template, request, redirect, url_for
)

bp = Blueprint('work', __name__, url_prefix='/work')

@bp.route('/', methods=('GET',))
def get_work_history():
    from workstory.work import repository as work_repository

    all_work = work_repository.get_all_works()

    work_history = {}
    for work_date, work_set in itertools.groupby(all_work, lambda w: w['work_date']):
        work_history[work_date] = list(work_set)

    work_history = dict(reversed(list(work_history.items())))

    return render_template('work/history.html', 
                           work_history=work_history)