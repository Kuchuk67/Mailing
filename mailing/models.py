from msilib import add_data
from multiprocessing.connection import Client

from django.db import models
from django.core.management.utils import get_random_secret_key
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.
class ClientName(models.Model):
    email = models.CharField(max_length=150, verbose_name="email клиента")
    name = models.CharField(max_length=150, verbose_name="Фамилия Имя Отчество")
    description  = models.TextField(verbose_name="Комментарий", null=True, blank=True,)
    unsubscribe = models.IntegerField( default=None, null=True, blank=True, editable=False,  verbose_name="Отписка")

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['name']


class Message(models.Model):
    title_mail = models.CharField(max_length=150, verbose_name="Тема письма")
    text_mail =  CKEditor5Field(verbose_name='Текст mail', config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="дата последнего изменения")

    def __str__(self):
        return f"{self.title_mail}"

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-created_at']

class Task(models.Model):
    name = models.CharField(max_length=150, verbose_name="имя задачи")
    start_at = models.DateTimeField(verbose_name="время начала рассылки")
    end_at = models.DateTimeField(verbose_name="время завершения рассылки")
    STATUS_CHOICES = [
        ('stop', 'Остановлена'),
        ('end', 'Завершена'),
        ('created', 'Создана'),
        ('start', 'Запущена'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='stop')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="message")

    def __str__(self):
        return f"{self.start_at} - {self.status}"

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-start_at']

class EmailForSend(models.Model):
    task = models.ForeignKey(Task,  on_delete=models.CASCADE, related_name="tasks")
    client = models.ForeignKey(ClientName,  on_delete=models.CASCADE, related_name="clients")
    token = models.CharField( max_length=50, default=get_random_secret_key() )

    def __str__(self):
        return {self.client}


class Attempt(models.Model):
    attempt_at = models.DateTimeField(auto_now_add=True, verbose_name="время рассылки")
    success = models.BooleanField(verbose_name='статус операции')
    response = models.CharField(max_length=250, verbose_name="ответ сервера")
    email_for_send = models.ForeignKey(EmailForSend, on_delete=models.CASCADE, related_name="mail_for_send")

    def __str__(self):
        return f"{self.email_for_send} - {self.success}"

    class Meta():
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'
        ordering = ['-attempt_at']