from mailing.models import Task
from datetime import datetime,timezone, timedelta

from mailing.services.send_email import send_email_to_clients

dt = datetime.now(timezone(timedelta(hours=3)))

def do_some_task():
  # Ищем задачу на отправку
  tasks = Task.objects.filter(start_at__gt=dt, status='created')

  for task in tasks:
    task.status = 'start'
    task.save()
    send_email_to_clients(task.user, task.id)
    task.status = 'Завершена'
    task.save()
    print(f"Рассылка {task} завершена")






#print(dt)