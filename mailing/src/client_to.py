from django.db import IntegrityError

from config.settings import BASE_DIR
import json
import os
from mailing.models import ClientName, EmailForSend
from typing import Optional
import secrets


class ClientTo():
    """ Получает адреса клиентов   из файла JSON.
    Установит атрибут self.json - при инициализации в него  загружается словарь е-mail'ов клиентов
    по умолчанию из mailing/data/client.json. или указать file_json='client_new.json'
    Методы: create_email_for_send - добавит mail в список(если его там нет) и привяжет к рассылке с ID указаному в параметре task_id ,
    insert_clients - только добавит в список(если его там нет).
    Установит атрибуты: self.count_all - обработанные клиенты,
    self.count_ok -  успешно добавленные клиенты,
    self.count_error - количество ошибок при обработке.
    """

    # Атрибуты метода
    @staticmethod
    def remove():
        ClientTo.count_all = 0  # Всего обработано адресов
        ClientTo.count_error = 0  # Ошибка при обработке адреса
        ClientTo.count_add = 0  # Добавлено новых в список адресов
        ClientTo.count_update = 0  # Обновлено в списке адресов
        ClientTo.count_ok = 0  # Успешно Обработанные адреса
        ClientTo.count_duble = 0  # Такие адреса уже в списке

    def __init__(self, task_id:int=0, file_json='client.json'):

        self.file_json = file_json # имя файла с адресами
        self.task_id = task_id  # ID рассылки при привязке адреса к рассылке
        ClientTo.remove()

        # Читать JSON из файла
        fail_name_json = os.path.join(BASE_DIR, 'mailing', 'data', self.file_json)
        with open(fail_name_json, 'r', encoding='utf8') as file:
            try:
                data = json.load(file)
            except Exception as e:
                print(e)
            self.json = data



    @staticmethod
    def find_client(client_email, client_name, user_id, client_description='') -> tuple[str, str, int]:


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
                client = ClientName.objects.create( email=client_email, user=user_id, name=client_name, description=client_description)
                client.save()
                status = 'new'
            except Exception as e:
                print(e, "Ошибка: не добавлен клиент ", client_email, user_id, client_name, client_description)
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
        return client.email, status, client.id


    def create_email_for_send(self, user_id):
        """ Наполняет связующую таблицу е-mail'ов и рассылки (self.task_id)
        Наполняет таблицу EmailForSend
        Если пользователя нет в списке Client - добавляет его.
        """
        ClientTo.remove()

        # Взять данные одного клиента
        for client in self.json.values():
            self.count_all += 1

            # Найти его email в таблице, если нет - добавить
            email = ClientTo.find_client(client['email'], client['name'], user_id, client.get('description'))
            if email :
                # Добавить в таблицу EmailForSend
                token = secrets.token_urlsafe(20)
                try:
                    EmailForSend.objects.create(client_id=email[2], task_id=self.task_id, token=token)
                except IntegrityError:
                    self.count_duble += 1

                else:
                    self.count_ok += 1
                #email_to_send.save()

            else:
                self.count_error += 1
        # Взять данные следующего клиента


    def insert_clients(self, user_id):
        """ Добавляет пользователя в таблицу Client"""
        ClientTo.remove()

        # Взять данные одного клиента
        for client in self.json.values():
            self.count_all += 1
            # Найти его ID в таблице, если нет - добавить
            email,status, id_ = ClientTo.find_client(client.get('email'), client.get('name'), user_id,  client.get('description'))
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






