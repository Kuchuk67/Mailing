from django.core.management.base import BaseCommand
from users.models import CustomUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

class Command(BaseCommand):


    def handle(self, *args, **kwargs):
        CustomUser.objects.all().delete()

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
        #ct = ContentType.objects.get_for_model(Product)
        #model_add_perm = Permission.objects.get(name='Может отменять публикацию продукта',
                                                #codename='can_unpublish_product', content_type=ct)
        #new_group.permissions.add(model_add_perm)
        #print("Подключили can_unpublish")
        user2 = CustomUser.objects.create(
            username='Модератор Василий',
            email='moder@mail.ru',
        )
        user2.set_password('12345')
        user2.groups.add(new_group)
        user2.save()





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

#asdsDD24#$re
