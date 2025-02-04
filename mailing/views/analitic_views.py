from django.shortcuts import redirect, render
from django.views import View
from mailing.models import ClientName, Message, Task, EmailForSend

from mailing.src.client_to import ClientTo


class AnaliticView(View):
    def get(self, request, *args, **kwargs):
        # Собираем аналитику
        # количество писем
        count_clients = ClientName.objects.count()
        count_clients_active = ClientName.objects.filter(unsubscribe=0).count()
        clients_unsubscribe = count_clients - count_clients_active


        return render(request, 'mailing/index.html',
                      {'count_clients': count_clients,
                       'clients_unsubscribe': clients_unsubscribe,
                       'count_clients_active' : count_clients_active})
