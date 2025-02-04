from config.settings import BASE_DIR
import json
import os
from mailing.models import ClientName, EmailForSend
from typing import Optional
import secrets


class ClientTo:
    """ Получает JSON из файла и ID  рассылки.
    атрибут self.json - при инициализации загружается словарь е-mail'ов клиентов
    из mailing/data/client.json
    методы create_email_for_send, insert_clients
    self.count_all - обработанные клиенты
    self.count_error - количество ошибок при обработке
    """


    def __init__(self, task_id):
        # Читать JSON из файла
        fail_name_json = os.path.join(BASE_DIR, 'mailing', 'data', 'client.json')
        with open(fail_name_json, 'r', encoding='utf8') as file:
            try:
                data = json.load(file)
            except Exception as e:
                print(e)
            self.json = data
        self.task_id = task_id
        self.count_all = 0
        self.count_error = 0


    @staticmethod
    def find_client(client_email, client_name, client_description='') -> Optional[str]:
        """ Находит пользователя в таблице Client по e-mail'у, если нет - добавляет."""
        client = ClientName.objects.filter(email=client_email).first()
        if client is None:
            try:
                client = ClientName.objects.create(email=client_email, name=client_name, description=client_description)
                client.save()
            except Exception as e:
                print(e, "Ошибка: не добавлен клиент ", client_email, client_name, client_description)
                client.email = None
        else:
            # если данные не сходятся перезаписываем
            save = False
            if client.name != client_name:
                client.name = client_name
                save = True
            if client_description != client.description:
                client.description = client_description
                save = True
            if save:
                client.save()
        return client.email


    def create_email_for_send(self):
        """ Создает связующую таблицу е-mail'ов и рассылки (self.task_id)
        Наполняет таблицу EmailForSend
        Если пользователя нет в таблице Client - добавляет.
        """
        self.count_all = 0
        self.count_error = 0
        # Взять данные одного клиента
        for client in self.json.values():
            self.count_all += 1
            # Найти его email в таблице, если нет - добавить
            email = ClientTo.find_client(client['email'], client['name'], client['description'])
            if email :
                # Добавить в таблицу EmailForSend
                token = secrets.token_urlsafe(50)
                email_to_send = EmailForSend.objects.create(client=email, task=self.task_id, token=token)
                email_to_send.save()
                self.count_all += 1
            else:
                self.count_error += 1
        # Взять данные следующего клиента


    def insert_clients(self):
        """ Добавляет пользователя в таблицу Client"""
        self.count_all = 0
        self.count_error = 0
        # Взять данные одного клиента
        for client in self.json.values():
            self.count_all += 1
            # Найти его ID в таблице, если нет - добавить
            email = ClientTo.find_client(client['email'], client['name'], client['description'])
            if not email:
                self.count_error += 1
        # Взять данные следующего клиента



x = ClientTo(5)
print(x.task_id)
print(x.json)
x.create_email_for_send()

