from datetime import datetime

from django.core.mail import send_mail

from config import settings

from ..models import Attempt, ClientName, Task


def send_email_to_clients(user_pk, task_id) -> bool:
    """Отправляет почту клиентам.
    принимает id пользователя и id задачи-рассылки"""
    print("Отправка писем по задаче № ", task_id)
    print("пользователь ", user_pk)

    task_for_send = ClientName.objects.filter(
        emailforsend__task__user=user_pk, emailforsend__task=task_id
    )
    email_for_send = [task.email for task in task_for_send]

    task = Task.objects.get(user=user_pk, pk=task_id)

    data_send = datetime.now().astimezone()
    success = False

    send_status = send_mail(
        task.message.title_mail,
        task.message.text_mail,
        settings.EMAIL_HOST_USER,
        email_for_send,
        fail_silently=False,
    )
    if send_status > 0:
        task.end_at = data_send
        task.status = "end"
        task.save()
        success = True

    # Сохранение данных по отправке писем
    Attempt.objects.create(
        attempt_at=data_send,
        success=success,
        response=send_status,
        task_send=task,
        len_mail=len(email_for_send),
    )
    if send_status > 0:
        return True
    else:
        return False
