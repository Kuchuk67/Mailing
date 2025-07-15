from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from ..forms import ClientNameForm, DeleteObjectForm
from ..models import ClientName
from ..src.client_to import ClientTo


# @method_decorator(cache_page(60 * 15), name='dispatch')
class ClientNameListView(LoginRequiredMixin, ListView):
    model = ClientName
    context_object_name = "clients"
    paginate_by = 12
    template_name = "mailing/client/clientname_list.html"
    extra_context = {"active_menu": "client"}

    def get_queryset(self):
        queryset = cache.get("mail_list_queryset")
        if not queryset:
            queryset = super().get_queryset()
            cache.set(
                "mail_list_queryset", queryset, 60 * 15
            )  # Кешируем данные на 15 минут
        return ClientName.objects.filter(user=self.request.user)


class ClientNameCreateView(LoginRequiredMixin, CreateView):
    model = ClientName
    form_class = ClientNameForm
    success_url = reverse_lazy("mailing:clients")
    template_name = "mailing/client/clientname_form.html"
    extra_context = {"active_menu": "client"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавить нового клиента"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        cache.delete("mail_list_queryset")
        return super().form_valid(form)

    # Передаем через kwargs id юзера в Форму
    def get_form_kwargs(self):
        kwargs = super(ClientNameCreateView, self).get_form_kwargs()
        kwargs["initial"] = {"user": self.request.user.pk}
        return kwargs


class ClientNameUpdateView(LoginRequiredMixin, UpdateView):
    model = ClientName
    context_object_name = "client"
    template_name = "mailing/client/clientname_form.html"
    form_class = ClientNameForm
    success_url = reverse_lazy("mailing:clients")
    extra_context = {"active_menu": "client"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование клиента"
        cache.delete("mail_list_queryset")
        return context


class ClientNameDeleteView(LoginRequiredMixin, DeleteView):
    model = ClientName
    context_object_name = "client"
    success_url = reverse_lazy("mailing:clients")
    template_name = "mailing/client/clientname_confirm_delete.html"
    extra_context = {"active_menu": "client"}

    def post(self, request, *args, **kwargs):
        cache.delete("mail_list_queryset")
        return super().post(self, request, *args, **kwargs)


class UnsubscribeDetailView(LoginRequiredMixin, DetailView):
    model = ClientName
    context_object_name = "client"


class DeleteAllClientView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_id = self.request.user.pk
        if request.method == "POST":
            cache.delete("mail_list_queryset")
            # print("*********")
            form = DeleteObjectForm(request.POST)
            if form.is_valid():
                # Удаляем все объекты модели
                ClientName.objects.filter(user=user_id).delete()

                # Перенаправляем пользователя на другую страницу после удаления
                return redirect("mailing:clients")

    def get(self, request, *args, **kwargs):
        return render(
            request, "mailing/client/clientname_confirm.html", {"active_menu": "client"}
        )


class ClientNameInsert(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cache.delete("mail_list_queryset")
        json_mail = ClientTo()
        json_mail.insert_clients(request.user)

        return render(
            request,
            "mailing/client/clientname_insert_report.html",
            {
                "count_all": json_mail.count_all,
                "count_error": json_mail.count_error,
                "active_menu": "client",
                "count_add": json_mail.count_add,
                "count_update": json_mail.count_update,
                "count_ok": json_mail.count_ok,
            },
        )
