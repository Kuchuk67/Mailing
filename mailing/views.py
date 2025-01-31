from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import ClientName, Message, Task
from django.views.generic import ListView, DetailView
from django.shortcuts import render

# Create your views here.

# Views for model - ClientName


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


# Views for model Message


class MessageListView(ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'mailing/message/message_list.html'
    paginate_by = 15
    extra_context = {"active_menu": "messages"}


class MessageCreateView(CreateView):
    model = Message
    fields = ['title_mail', 'text_mail']
    success_url = reverse_lazy('mailing:messages')
    template_name = 'mailing/message/message_form.html'
    extra_context = {'title': "Создать новый текст рассылки",
                     "active_menu": "messages",}


class MessageUpdateView(UpdateView):
    model = Message
    fields = ['title_mail', 'text_mail',  ]
    success_url = reverse_lazy('mailing:messages')
    template_name = 'mailing/message/message_form.html'
    extra_context = {'title': "Редактировать текст рассылки",
                     "active_menu": "messages",}


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:messages')
    template_name = 'mailing/message/message_confirm_delete.html'
    extra_context = {"active_menu": "messages"}


# Views for model Task


class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    paginate_by = 25
    extra_context = {"active_menu": "task"}


class TaskDetailsView(DetailView):
    model = Task
    context_object_name = 'task'
    extra_context = {"active_menu": "task"}


class TaskCreateView(CreateView):
    model = Task
    fields = ['title_mail', 'text_mail', 'created_at', 'updated_at',]
    success_url = reverse_lazy('mailing:tasks')
    extra_context = {"active_menu": "task"}


class TaskUpdateView(UpdateView):
    model = Task
    fields = ['title_mail', 'text_mail', 'created_at', 'updated_at', ]
    success_url = reverse_lazy('mailing:task_details')
    extra_context = {"active_menu": "task"}


class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('mailing:tasks')
    extra_context = {"active_menu": "task"}
