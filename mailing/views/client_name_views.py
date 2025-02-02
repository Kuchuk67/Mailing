from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from ..models import ClientName, Message, Task
from django.views.generic import ListView, DetailView

class ClientNameListView(ListView):
    model = ClientName
    context_object_name = 'clients'
    paginate_by = 12
    template_name = 'mailing/client/clientname_list.html'
    extra_context = {"active_menu": "client"}


class ClientNameCreateView(CreateView):
    model = ClientName
    fields = ['email',  'name',  'description', ]
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
    fields = ['email',  'name',  'description']
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