from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from ..models import ClientName, Message, Task
from django.views.generic import ListView, DetailView
from django.views import View
from ..forms import ClientNameForm, DeleteObjectForm
from django.shortcuts import redirect, render
from ..src.client_to import ClientTo

class ClientNameListView(ListView):
    model = ClientName
    context_object_name = 'clients'
    paginate_by = 12
    template_name = 'mailing/client/clientname_list.html'
    extra_context = {"active_menu": "client"}


class ClientNameCreateView(CreateView):
    model = ClientName
    form_class = ClientNameForm
    success_url = reverse_lazy('mailing:clients')
    template_name = 'mailing/client/clientname_form.html'
    extra_context = {"active_menu": "client"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить нового клиента'
        return context


class ClientNameUpdateView(UpdateView):
    model = ClientName
    context_object_name = 'client'
    template_name = 'mailing/client/clientname_form.html'
    form_class = ClientNameForm
    success_url = reverse_lazy('mailing:clients')
    extra_context = {"active_menu": "client"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование клиента'
        return context


class ClientNameDeleteView(DeleteView):
    model = ClientName
    context_object_name = 'client'
    success_url = reverse_lazy('mailing:clients')
    template_name = 'mailing/client/clientname_confirm_delete.html'
    extra_context = {"active_menu": "client"}

class UnsubscribeDetailView(DetailView):
    model = ClientName
    context_object_name = 'client'

class DeleteAllClientView(View):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = DeleteObjectForm(request.POST)
            if form.is_valid():
                # Удаляем все объекты модели
                ClientName.objects.all().delete()
                # Перенаправляем пользователя на другую страницу после удаления
                return redirect('mailing:clients')
    def get(self, request, *args, **kwargs):
        return render(request, 'mailing/client/clientname_confirm.html', {"active_menu": "client"})



class ClientNameInsert(View):
    def get(self, request, *args, **kwargs):
        json_mail = ClientTo()
        json_mail.insert_clients()
        return render(request, 'mailing/client/clientname_insert_report.html',
                      {'count_all': json_mail.count_all,
                       'count_error': json_mail.count_error,
                       "active_menu": "client",
                       'count_add': json_mail.count_add,
                       'count_update': json_mail.count_update,
                       'count_ok': json_mail.count_ok
                       } )

