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
        # количество рассылок
        count_tasks_stop = Task.objects.filter(status='stop').count()
        count_tasks = Task.objects.filter().count()
        count_tasks_end = Task.objects.filter(status='end').count()
        count_tasks_active = count_tasks - (count_tasks_end + count_tasks_stop)
        return render(request, 'mailing/index.html',
                      {'count_clients': count_clients,
                       'clients_unsubscribe': clients_unsubscribe,
                       'count_clients_active' : count_clients_active,
                       'count_tasks_stop': count_tasks_stop,
                       'count_tasks': count_tasks,
                       'count_tasks_end': count_tasks_end,
                       'count_tasks_active': count_tasks_active,
                       })
