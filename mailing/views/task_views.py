from msilib.schema import Class

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from ..models import ClientName, Message, Task, EmailForSend
from django.views.generic import ListView, DetailView
from ..forms import TaskForm
from ..services.send_email import send_email_to_clients


# Views for model Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    paginate_by = 10
    template_name = 'mailing/tasks/task_list.html'
    extra_context = {"active_menu": "task"}

    def get(self, request, *args, **kwargs):

        if request.GET.get('send'):
            user_pk =  self.request.user.pk
            send_email_to_clients(user_pk, request.GET.get('send'))#request.GET.get('send')

        return  super(TaskListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_context_data(self):
        context = super().get_context_data()
        page = self.request.GET.get('page')
        context['page'] = page
        context['clients_counter'] = EmailForSend.objects.values('task_id').order_by('task_id').annotate(field_count=Count('task_id'))
        #print(context['clients_counter'])
        return context


class TaskDetailsView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    extra_context = {"active_menu": "task"}


class TaskCreateView(LoginRequiredMixin,  CreateView):

    # передаем в форму грёбаного пользователя
    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(TaskCreateView, self).get_form_kwargs()
        form_kwargs['initial'] = {'user_pk':  self.request.user.pk}
        return form_kwargs

    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('mailing:tasks')
    extra_context = {"active_menu": "task"}
    template_name = 'mailing/tasks/task_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('mailing:tasks')
    extra_context = {"active_menu": "task"}
    template_name = 'mailing/tasks/task_form.html'

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(TaskUpdateView, self).get_form_kwargs()
        form_kwargs['initial'] = {'user_pk':  self.request.user.pk}
        return form_kwargs


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('mailing:tasks')
    extra_context = {"active_menu": "task"}
    template_name = 'mailing/tasks/task_confirm_delete.html'


