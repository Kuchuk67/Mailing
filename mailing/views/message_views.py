from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from ..models import ClientName, Message, Task
from django.views.generic import ListView, DetailView

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
