from django.core.mail import send_mail
from config import settings
from ..models import ClientName, Message, Task, EmailForSend
import datetime

def send_email_to_clients(self, task):
    """ Отправляет почту клиентам.
    принимает сущность 'задачи' """
    print('Отправка писем по задаче № ',task)
    print('пользователь ',self.request.user.pk)
    #print(task)
    task_for_send = ClientName.objects.filter(emailforsend__task__user=self.request.user.pk, emailforsend__task=task )
    task = Task.objects.get(pk=task, user=self.request.user.pk)

    #for task in task_for_send:
     #   print(task.email)
    list_mails = [task.email for task in task_for_send]
    print(list_mails)
    #print(task_for_send.name)
    #print(dir(task_for_send.client_emails))
    #print(mail_message.message.text_mail)
    status = 0
    if list_mails and task.message.text_mail:

        status = send_mail(
            task.message.title_mail,
            task.message.text_mail,
            settings.EMAIL_HOST_USER,
            list_mails,
            fail_silently=False,
        )
    if status >0:
        # Записать дату рассылки
        from django.utils import timezone
        task.end_at = timezone.make_aware(datetime.datetime.now())
        task.save()
        # Записать отчет по рассылки


        #print(datetime.datetime.now())
            #mail_message.message.text_mail
