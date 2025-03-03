from django.shortcuts import render, redirect
from ..forms import ClientNameForm, DeleteObjectForm
from ..models import ClientName, Message, Task, EmailForSend
from django.views.generic import ListView, DetailView
from ..forms import TaskForm
from django.views import View
from ..src.client_to import ClientTo

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
        task_id = self.kwargs['task']
        context['task_id'] = task_id
        return context

class EmailForSendInsertView(View):
    #model = EmailForSend
    def get(self, request, *args, **kwargs):
        task_id = int(self.kwargs['task'])
        json_mail = ClientTo(task_id=task_id, file_json='client_new.json')
        #user_id = self.request.user.pk
        json_mail.create_email_for_send(self.request.user)
        return render(request, 'mailing/tasks/clientname_insert_report.html',
                      {'count_all': json_mail.count_all,
                       'count_error': json_mail.count_error,
                       "active_menu": "task",
                       'count_duble': json_mail.count_duble,
                       #'count_update': json_mail.count_update,
                       'count_ok': json_mail.count_ok,
                       'task_id': task_id,
                       } )


class EmailForSendDeleteView(View):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = DeleteObjectForm(request.POST)
            if form.is_valid():
                # Удаляем все объекты модели
                EmailForSend.objects.filter(task_id=kwargs['task']).delete()
                # Перенаправляем пользователя на другую страницу после удаления
                return redirect('mailing:tasks')
    def get(self, request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs['task'])
        return render(request, 'mailing/tasks/email_confirm.html',
                      {"active_menu": "task",
                               "task" : task,
                       })
