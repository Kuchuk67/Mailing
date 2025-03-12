from django.core.management.base import BaseCommand
from users.models import CustomUser
from mailing.models import Task
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):


    def handle(self, *args, **kwargs):
        CustomUser.objects.all().delete()

        #Создаем суперпользователя
        user = CustomUser.objects.create(
            username='admin',
            email='admin@mail.ru',
        )
        user.set_password('12345')
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()


        # Создаем новую группу
        new_group, created = Group.objects.get_or_create(name='Модератор')

        print('Создаем новую группу', new_group, created)

        ct = ContentType.objects.get_for_model(CustomUser)
        #
        permission=Permission.objects.create(codename='can_moderation_users', name='Модерировать пользователей', content_type=ct)
        new_group.permissions.add(permission)
        ct = ContentType.objects.get_for_model(Task)
        permission = Permission.objects.create(codename='can_moderation_mailing', name='Модерировать рассылки',
                                               content_type=ct)
        new_group.permissions.add(permission)
        #permission = Permission.objects.get(codename='view_customuser', content_type=ct)

        #new_group.permissions.add(permission)
        #permission = Permission.objects.create(codename='can_change_user', name='Может реактировать пользователей', content_type=ct)
        #new_group.permissions.add(permission)
        print("Подключили пермишены")

        user2 = CustomUser.objects.create(
            username='Модератор Василий',
            email='moder@mail.ru',
        )
        user2.set_password('12345')
        user2.groups.add(new_group)
        user2.save()

        user3 = CustomUser.objects.create(
            username='Пользователь',
            email='user@mail.ru',
        )
        user3.set_password('12345')
        user3.save()





        """CustomUser.objects.get_or_create(
                pk=1,
                username='admin',
                email='kuchukov.s@mail.ru',
                password='12345',
                is_staff=True,
                is_superuser=True,
            )"""



    """
        CustomUser.objects.get_or_create(
            pk=2,
            username='Модератор Василий',
            email='moder@mail.ru',
            password='12345',
        )
        CustomUser.objects.get_or_create(
            pk=3,
            username='User',
            email='user@mail.ru',
            password='12345',
        )"""
