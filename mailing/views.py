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


"""class ClientNameDetailsView(DetailView):
    model = ClientName
    context_object_name = 'client'
    template_name = 'mailing/client/clientname_detail.html'"""


class ClientNameCreateView(CreateView):
    model = ClientName
    fields = ['email',  'name',  'description',  'unsubscribe',]
    success_url = reverse_lazy('mailing:clients')


class ClientNameUpdateView(UpdateView):
    model = ClientName
    fields = ['email',  'name',  'description',  'unsubscribe',]
    success_url = reverse_lazy('mailing:client_details')


class ClientNameDeleteView(DeleteView):
    model = ClientName
    success_url = reverse_lazy('mailing:clients')


class UnsubscribeDetailView(DetailView):
    model = ClientName
    context_object_name = 'client'


# Views for model Message


class MessageListView(ListView):
    model = Message
    context_object_name = 'messages'
    paginate_by = 25


class MessageDetailsView(DetailView):
    model = Message
    context_object_name = 'message'


class MessageCreateView(CreateView):
    model = Message
    fields = ['title_mail', 'text_mail', 'created_at', 'updated_at',]
    success_url = reverse_lazy('mailing:messages')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ['title_mail', 'text_mail', 'created_at', 'updated_at', ]
    success_url = reverse_lazy('mailing:message_details')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:messages')


# Views for model Task


class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    paginate_by = 25


class TaskDetailsView(DetailView):
    model = Task
    context_object_name = 'task'


class TaskCreateView(CreateView):
    model = Task
    fields = ['title_mail', 'text_mail', 'created_at', 'updated_at',]
    success_url = reverse_lazy('mailing:tasks')


class TaskUpdateView(UpdateView):
    model = Task
    fields = ['title_mail', 'text_mail', 'created_at', 'updated_at', ]
    success_url = reverse_lazy('mailing:task_details')


class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('mailing:tasks')
