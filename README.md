# Mailing
приложение для организации рассылок по электронной почте

## Аналитика

## Клиенты
Выводит список адресов для рассылок. 
Возможность добавления и редактирования данных клиента, добавлять комментарии.
Загрузка списка клиентов из JSON-файла.
Удаление всех данных.

## Тексты
Содержит базу текстов для рассылок.
Возможность добавления и редактирования текстов через
визуальные редактор ck-editor.

## Планировка рассылок
Содержит функционал для создания задачи по организации рассыкци.
Основные параметры:
* Время начала и время завершения рассылки.
* Текст сообщения: Подключается текстовая информация рассылки из базы текстов.
* Статус рассылки.

#### Статус рассылки:
1. **Остановлена** - Данная рассылка отключена и не будет никогда запущена.
2. **Создана** - рассылка включена, но не отправляла писем и ожидает время старта
3. **Запущена** - рассылка включена и уже отправила хотя бы одно письмо
4. **Завершена** - рассылка завершилась по истечению времени работы или отправлены все письма



## Установка

python manage.py  makemigrations
```commandline
python manage.py  migrate
```
```commandline
python manage.py createsuperuser
```

python  -Xutf8 manage.py dumpdata mailing.ClientName --output test_data/ClientName_fixture.json --indent 4
python  -Xutf8 manage.py dumpdata mailing.Message --output test_data/Message_fixture.json --indent 4
python -Xutf8 manage.py dumpdata mailing.Task --output test_data/Task_fixture.json --indent 4

### Загрузить тестовые данные
```commandline
python manage.py loaddata test_data/ClientName_fixture.json
```
```commandline
python manage.py loaddata test_data/Message_fixture.json
```
```commandline
python manage.py loaddata test_data/Task_fixture.json

```

