from django.core.mail import send_mail
from config import settings
from ..models import ClientName, Message, Task, EmailForSend

def send_email_to_clients(self, task):
    """ Отправляет почту клиентам.
    принимает сущность 'задачи' """
    print('Отправка писем по задаче № ',task)
    print('пользователь ',self.request.user.pk)
    #print(task)
    task_for_send = ClientName.objects.filter(emailforsend__task__user=self.request.user.pk, emailforsend__task=task )
    print(task_for_send)

    #print(task_for_send.name)
    #print(dir(task_for_send.client_emails))

    '''send_mail(
        f"Регистрация в сервисе рассылок",
        f"""Вы зарегистрированы на сервисе рассылок
                Поддтвердите ваш e-mail перейди по ссылке
                <a href="{settings.BASE_HOSTS}/mailing/users/activate?token={token}">{settings.BASE_HOSTS}/mailing/users/activate?token={token}</a>
    Ваш логин e-mail: {mail_to}""",
        settings.EMAIL_HOST_USER,
        (mail_to,),
        fail_silently=False,
    )'''
