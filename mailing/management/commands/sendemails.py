from django.core.management.base import BaseCommand
from mailing.services.send_email import send_email_to_clients
from users.models import CustomUser
from mailing.models import Task, Attempt


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        user_email = input('Введите email пользователя:')

        # получение данных о пользователе
        try:
            user = CustomUser.objects.get(email=user_email)
        except:
            print("При получении данных о пользователе возника ошибка. Возможно такой email не существует.")
            return None

        # получение данных о pассылоках пользователя
        try:
            tasks = Task.objects.filter(user=user.pk)
        except:
            print("Рассылок связанных с этим пользователем не найдено.")
            return None

        # Выбор номера рассылки для отправки
        print("Найдены рассылки:\n")
        for task in tasks:
            print( f"{task.pk}. {task.name}  /  {task}" )
        task_for_send = input('\nВведите номер рассылки для отправки или 0 для выхода:')
        if task_for_send == "0":
            return None

        # Отправка
        try:
            send_status = send_email_to_clients(user.pk, task_for_send)
        except:
            print("Рассылок связанных с этим пользователем не найдено.")
            return None

        if send_status:
            print("\n\nРассылка успешно завершена\n")





