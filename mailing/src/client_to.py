from config.settings import BASE_DIR
import json
import os
from mailing.models import ClientName, EmailForSend
from typing import Optional
import secrets


class ClientTo():
    """ Получает адреса клиентов   из файла JSON.
    атрибут self.json - при инициализации в него  загружается словарь е-mail'ов клиентов
    по умолчанию из mailing/data/client.json. или указать file_json='client_new.json'
    Методы create_email_for_send, insert_clients.
    Установит атрибуты: self.count_all - обработанные клиенты,
    self.count_ok -  успешно добавленные клиенты,
    self.count_error - количество ошибок при обработке.
    """


    def __init__(self, task_id=0, file_json='client.json'):
        # Читать JSON из файла
        self.file_json = file_json
        fail_name_json = os.path.join(BASE_DIR, 'mailing', 'data', self.file_json)
        with open(fail_name_json, 'r', encoding='utf8') as file:
            try:
                data = json.load(file)
            except Exception as e:
                print(e)
            self.json = data
        self.task_id = task_id
        self.count_all = 0
        self.count_error = 0
        self.count_add = 0
        self.count_update = 0
        self.count_ok = 0


    @staticmethod
    def find_client(client_email, client_name, client_description='') -> tuple[str, str]:
        """ Находит пользователя в таблице Client по e-mail'у, если нет - добавляет.
        Возвращает email, статус:
        new - новый клиент;
        error - ошибка при добавлении;
        ok - клиент найден;
        update - обновление данных клиента."""
        client_email = client_email.strip()
        client = ClientName.objects.filter(email=client_email).first()
        if client is None:
            try:
                client = ClientName.objects.create(email=client_email, name=client_name, description=client_description)
                client.save()
                status = 'new'
            except Exception as e:
                print(e, "Ошибка: не добавлен клиент ", client_email, client_name, client_description)
                client.email = ''
                status = 'error'
        else:
            # если данные не сходятся перезаписываем
            status = 'ok'
            save = False
            if client.name != client_name:
                client.name = client_name
                save = True
            if client_description != client.description:
                client.description = client_description
                save = True
            if save:
                client.save()
                status = 'update'
        return client.email, status


    def create_email_for_send(self):
        """ Создает связующую таблицу е-mail'ов и рассылки (self.task_id)
        Наполняет таблицу EmailForSend
        Если пользователя нет в таблице Client - добавляет.
        """
        self.count_all = 0
        self.count_error = 0
        self.count_add = 0
        self.count_update = 0
        self.count_ok = 0

        # Взять данные одного клиента
        for client in self.json.values():
            self.count_all += 1
            # Найти его email в таблице, если нет - добавить
            email = ClientTo.find_client(client['email'], client['name'], client.get('description'))
            if email :
                # Добавить в таблицу EmailForSend
                token = secrets.token_urlsafe(20)

                email_to_send = EmailForSend.objects.create(client_id=email[0], task_id=self.task_id, token=token)
                #email_to_send.save()
                self.count_ok += 1
            else:
                self.count_error += 1
        # Взять данные следующего клиента


    def insert_clients(self):
        """ Добавляет пользователя в таблицу Client"""
        self.count_all = 0
        self.count_error = 0
        self.count_add = 0
        self.count_update = 0
        self.count_ok = 0
        # Взять данные одного клиента
        for client in self.json.values():
            self.count_all += 1
            # Найти его ID в таблице, если нет - добавить
            email,status = ClientTo.find_client(client.get('email'), client.get('name'), client.get('description'))
            # сохраняем результат
            if status == 'error':
                self.count_error += 1
            if status == 'new':
                self.count_add += 1
            if status == 'update':
                self.count_update += 1
            if status == 'ok':
                self.count_ok += 1


        # Взять данные следующего клиента






