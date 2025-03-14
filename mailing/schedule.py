from .task import do_some_task
from apscheduler.schedulers.background import BackgroundScheduler
from config.settings import scheduler

def cancel_task(id_task):
    try:
        scheduler.remove_job(job_id=id_task)
    except Exception:
        pass

def start_task(start_at, id_task):
    cancel_task(id_task)
    job = scheduler.add_job(do_some_task, 'date', run_date=start_at, id=id_task)
    print(type(job), job)

