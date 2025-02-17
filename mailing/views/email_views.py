from ..models import ClientName, Message, Task, EmailForSend
from django.views.generic import ListView, DetailView
from ..forms import TaskForm


class EmailForSendView(ListView):
    model = EmailForSend
    context_object_name = 'clients'
    paginate_by = 25
    template_name = 'mailing/tasks/task_for_clients.html'
    extra_context = {"active_menu": "task"}


    # Получаем связанные данные: mail-ы куда отправлять рассылку
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        task = self.kwargs['task']
        return queryset.order_by('task_id').filter(task_id=task)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # page чтобы вернутся на предыдущую страницу
        page = self.request.GET.get('page')
        context['page'] = page
        return context

