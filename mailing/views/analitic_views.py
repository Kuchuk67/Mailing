from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from mailing.models import ClientName, Attempt, Task
from django.db.models import Sum


def home(request):
    if request.method == "GET":

        return render(request, "home.html")


class AnaliticView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """print(request.user.groups.all())
        group_user = request.user.groups.all()
        moderator = False
        for g in group_user:
            if g == 'Модератор':
                moderator = True"""

        # Собираем аналитику
        # количество писем
        # print(request.user.pk)
        count_clients = ClientName.objects.filter(user=request.user.pk).count()
        count_clients_active = ClientName.objects.filter(unsubscribe=0, user=request.user.pk).count()
        clients_unsubscribe = count_clients - count_clients_active
        # количество рассылок
        count_tasks_stop = Task.objects.filter(user=request.user.pk, status="stop").count()
        count_tasks = Task.objects.filter(user=request.user.pk).count()
        count_tasks_end = Task.objects.filter(user=request.user.pk, status="end").count()
        count_tasks_active = count_tasks - (count_tasks_end + count_tasks_stop)
        # количество отправленных писем
        email_send_ок = Attempt.objects.filter(task_send__user_id=request.user.pk).aggregate(total=Sum("len_mail"))[
            "total"
        ]
        # values('len_mail').sum)

        # print (email_send_ок)

        return render(
            request,
            "mailing/index.html",
            {
                "count_clients": count_clients,
                "clients_unsubscribe": clients_unsubscribe,
                "count_clients_active": count_clients_active,
                "count_tasks_stop": count_tasks_stop,
                "count_tasks": count_tasks,
                "count_tasks_end": count_tasks_end,
                "count_tasks_active": count_tasks_active,
                "email_send_ок": email_send_ок,
            },
        )
