from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from ..models import Message, Task
from django.views.generic import ListView
from ..forms import MessageForm
from django.db.models import Count

# Views for model Message


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = "messages"
    template_name = "mailing/message/message_list.html"
    paginate_by = 15
    extra_context = {"active_menu": "messages"}

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Подсчет сколько созданных рассылок используют этот текст
        counter_message = Task.objects.values("message").order_by("message").annotate(field_count=Count("message"))
        context["counter_message"] = counter_message
        return context


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:messages")
    template_name = "mailing/message/message_form.html"
    extra_context = {
        "title": "Создать новый текст рассылки",
        "active_menu": "messages",
    }

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:messages")
    template_name = "mailing/message/message_form.html"
    extra_context = {
        "title": "Редактировать текст рассылки",
        "active_menu": "messages",
    }

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:messages")
    template_name = "mailing/message/message_confirm_delete.html"
    extra_context = {"active_menu": "messages"}
