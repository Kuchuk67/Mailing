from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from ..models import ClientName, Message, Task
from django.views.generic import ListView, DetailView
from ..forms import MessageForm

# Views for model Message


class MessageListView(ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'mailing/message/message_list.html'
    paginate_by = 15
    extra_context = {"active_menu": "messages"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # перебираем все записи
        for message in context['messages']:
            # и что-то с ними делаем....
            print(message.pk)
            x = Task.objects.filter(message=message.pk).count()
            print(x)
        print("+++")
        x = Task.objects.all().distinct().count()
            # self.object.task_set.all()
        # print(context['messages'][0].text_mail)
        return context


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')
    template_name = 'mailing/message/message_form.html'
    extra_context = {'title': "Создать новый текст рассылки",
                     "active_menu": "messages",}


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')
    template_name = 'mailing/message/message_form.html'
    extra_context = {'title': "Редактировать текст рассылки",
                     "active_menu": "messages",}


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:messages')
    template_name = 'mailing/message/message_confirm_delete.html'
    extra_context = {"active_menu": "messages"}
