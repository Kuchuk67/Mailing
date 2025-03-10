from django.core.mail import send_mail
from datetime import datetime

from config import settings
from ..models import ClientName, Attempt, Task, EmailForSend

def send_email_to_clients(self, task_id):
    """ Отправляет почту клиентам.
    принимает сущность 'задачи' """
    print('Отправка писем по задаче № ',task_id)
    print('пользователь ',self.request.user.pk)

    task_for_send = ClientName.objects.filter(emailforsend__task__user=self.request.user.pk, emailforsend__task=task_id )
    email_for_send = [task.email for task in task_for_send]

    task = Task.objects.get(user=self.request.user.pk, pk=task_id )

    data_send = datetime.now().astimezone()
    success = False

    send_status = send_mail(
        task.message.title_mail,
        task.message.text_mail,
        settings.EMAIL_HOST_USER,
        email_for_send,
        fail_silently=False,
    )
    if send_status >0:
        task.end_at = data_send
        task.status = 'end'
        task.save()
        success = True

    # Сохранение данных по отправке писем
    attempt = Attempt.objects.create(attempt_at=data_send,
                            success = success,
                            response = send_status,
                            task_send = task,
                            len_mail = len(email_for_send),
    )


