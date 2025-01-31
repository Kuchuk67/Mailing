# Mailing
приложение для организации рассылок по электронной почте


python  -Xutf8 manage.py dumpdata mailing.ClientName --output ClientName_fixture.json --indent 4
python  -Xutf8 manage.py dumpdata mailing.Message --output Message_fixture.json --indent 4
python -Xutf8 manage.py dumpdata mailing.Task --output Task_fixture.json --indent 4

python manage.py loaddata ClientName_fixture.json

