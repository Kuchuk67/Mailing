# Mailing
приложение для организации рассылок по электронной почте


python manage.py  makemigrations
python manage.py  migrate
python manage.py createsuperuser


python  -Xutf8 manage.py dumpdata mailing.ClientName --output /test_data/ClientName_fixture.json --indent 4
python  -Xutf8 manage.py dumpdata mailing.Message --output /test_data/Message_fixture.json --indent 4
python -Xutf8 manage.py dumpdata mailing.Task --output /test_data/Task_fixture.json --indent 4

python manage.py loaddata /test_data/ClientName_fixture.json

