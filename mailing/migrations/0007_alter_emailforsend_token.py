# Generated by Django 5.1.5 on 2025-02-02 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0006_alter_emailforsend_token_alter_message_text_mail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailforsend',
            name='token',
            field=models.CharField(default='rj!#)=-)86g=0o4^rth7w$=pmjutuof0^zrt2m2ayr-@-&f+(!', max_length=50),
        ),
    ]
