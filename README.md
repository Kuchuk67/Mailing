# Mailing
#### Pyton, Django, Postgres, bootstrap, Redis

приложение для организации рассылок по электронной почте


## !!! Приложение работает в тестовом режиме
**Почта выводится в консоль. Для отправки почты через SMTP  
измените значение EMAIL_BACKEND 
в файле config/settings.py страница 26-28** 
и заполните данные доступа к SMTP-серверу в .env

### Функция отправки почты
Отправить рассылку из командной строки
```commandline
python manage.py sendemails
```




## Аналитика
Выводит данные по рассылкам
#### Подписчики 
количество клиентов в базе

_Для будущей возможности расширения функционала
предусмотренно поле "отписавшиеся от рассылки"_ 

#### Рассылки
Активные и завершенные рассылки

#### Отправлено писем
Сколько писем отправлено данным клиентом

## Клиенты
Выводит список адресов для рассылок для данного клиета. 
Возможность добавления и редактирования данных клиента, добавлять комментарии.
Загрузка списка клиентов из JSON-файла.
Удаление всех данных.

## Тексты
Содержит базу текстов для рассылок.
Возможность добавления и редактирования текстов через
визуальные редактор CK-Editor.

## Планировка рассылок
Содержит функционал для создания задачи по организации рассыкци.
Основные параметры:
* Время начала и время завершения рассылки.
* Текст сообщения: Подключается текстовая информация рассылки из базы текстов.
* Статус рассылки.
Возможность загрузки новых клиентов из файла json - client_new.json

#### Статус рассылки:
1. **Остановлена** - Данная рассылка отключена и не будет никогда запущена.
2. **Создана** - рассылка включена, но не отправляла писем и ожидает время старта
3. **Запущена** - рассылка включена и уже отправила хотя бы одно письмо
4. **Завершена** - рассылка завершилась по истечению времени работы или отправлены все письма



# Установка Проекта

Проект разработан под управлением poetry
Однако проект так же содержит актуальный файл [requirements.txt](requirements.txt)

### Активация виртуального окружения
```commandline
 poetry shell
```
Установка пакетов
```commandline
 poetry install
```
### Настроить файл .env 
по образцу (.env.example)

### Миграции

```commandline
 python manage.py  migrate
```




### Загрузить тестовые данные

### Создать тестовых пользователей
```commandline
python manage.py add_user  
```
Группа - Модераторы
Администратор - admin@mail.ru - 12345
Модератор - moder@mail.ru - 12345
User - user@mail.ru - 12345

Клиенты
```commandline
 python manage.py loaddata test_data/ClientName_fixture.json
```
Тексты для писем
```commandline
 python manage.py loaddata test_data/Message_fixture.json
```
Запланированные рассылки
```commandline
 python manage.py loaddata test_data/Task_fixture.json
```
Подключенные email-ы к рассылкам
```commandline
 python manage.py loaddata test_data/EmailForSend_fixture.json
```
Логи
```commandline
 python manage.py loaddata test_data/Attempt_fixture.json
```

## Ввод клиентской базы
* Адреса для рассылки вводятся в разделе клиенты кнопкой добавить.

_Так же возможна загрузки из json-файла расположенного в папке data - client.json
Данный функционал предусмотрен для добавления в будущем
возможности загрузки клиентской база посредством файла._

* Клиентскую базу можно загрузить непосредственно в процессе планировки рассылки.

_Так же возможна загрузки из json-файла расположенного в папке data - client_new.json
Данный функционал предусмотрен для добавления в будущем
возможности загрузки клиентской база посредством файла._




## Кеширование Redis


Низкоуровневое кеширование запроса
`class ClientNameListView`

`class EmailForSendView`

\+ удаление кеша при обновлении записей.

`class EmailForSendView, class EmailForSendInsertView
`
и классы в файле client_name_views.py 





python  -Xutf8 manage.py dumpdata mailing.ClientName --output test_data/ClientName_fixture.json --indent 4
python  -Xutf8 manage.py dumpdata mailing.Message --output test_data/Message_fixture.json --indent 4
python -Xutf8 manage.py dumpdata mailing.Task --output test_data/Task_fixture.json --indent 4
python -Xutf8 manage.py dumpdata mailing.EmailForSend --output test_data/EmailForSend_fixture.json --indent 4
python -Xutf8 manage.py dumpdata mailing.Attempt --output test_data/Attempt_fixture.json --indent 4


