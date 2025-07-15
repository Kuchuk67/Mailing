import secrets

from django.core.cache import cache
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView

from ..forms import DeleteObjectForm
from ..models import ClientName, EmailForSend, Task
from ..src.client_to import ClientTo


class EmailForSendView(ListView):
    model = EmailForSend
    context_object_name = "clients"
    paginate_by = 25
    template_name = "mailing/tasks/task_for_clients.html"
    extra_context = {"active_menu": "task"}

    # Получаем связанные данные: mail-ы куда отправлять рассылку
    def get_queryset(self, **kwargs):

        queryset = cache.get("email_for_send")
        task = self.kwargs["task"]
        if not queryset:  # Кешируем данные на 15 минут
            queryset = super().get_queryset()
            cache.set("email_for_send", queryset, 60 * 15)
        return queryset.order_by("task_id").filter(task_id=task)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # page чтобы вернутся на предыдущую страницу
        page = self.request.GET.get("page")
        context["page"] = page
        task_id = self.kwargs["task"]
        context["task_id"] = task_id
        return context


class EmailForSendInsertView(View):
    # model = EmailForSend
    def get(self, request, *args, **kwargs):
        # Сброс кеша
        cache.delete("email_for_send")

        task_id = int(self.kwargs["task"])
        json_mail = ClientTo(task_id=task_id, file_json="client_new.json")
        # user_id = self.request.user.pk
        json_mail.create_email_for_send(self.request.user)
        return render(
            request,
            "mailing/tasks/clientname_insert_report.html",
            {
                "count_all": json_mail.count_all,
                "count_error": json_mail.count_error,
                "active_menu": "task",
                "count_duble": json_mail.count_duble,
                "count_ok": json_mail.count_ok,
                "task_id": task_id,
            },
        )


class EmailForSendDeleteView(View):
    def post(self, request, *args, **kwargs):
        # Сброс кеша
        cache.delete("email_for_send")

        if request.method == "POST":
            form = DeleteObjectForm(request.POST)
            if form.is_valid():
                # Удаляем все объекты модели
                EmailForSend.objects.filter(task_id=kwargs["task"]).delete()
                # Перенаправляем пользователя на другую страницу после удаления
                return redirect("mailing:tasks")

    def get(self, request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs["task"])
        return render(
            request,
            "mailing/tasks/email_confirm.html",
            {
                "active_menu": "task",
                "task": task,
            },
        )


class EmailForSendAddView(View):
    def get(self, request, *args, **kwargs):
        # Сброс кеша
        cache.delete("email_for_send")
        count_error, count_all, count_duble, count_ok = 0, 0, 0, 0
        task_id = int(self.kwargs["task"])
        token = secrets.token_urlsafe(20)
        user = self.request.user.pk
        client_mails = ClientName.objects.filter(user=user)
        for client in client_mails:
            print(client.email, user, task_id)
            count_all += 1
            try:
                EmailForSend.objects.create(
                    client_id=client.pk, task_id=task_id, token=token
                )
            except IntegrityError:
                count_duble += 1
                count_error += 1
            else:
                count_ok += 1
        return render(
            request,
            "mailing/tasks/clientname_insert_report.html",
            {
                "count_all": count_all,
                "count_error": count_error,
                "active_menu": "task",
                "count_duble": count_duble,
                # 'count_update': json_mail.count_update,
                "count_ok": count_ok,
                "task_id": task_id,
            },
        )
