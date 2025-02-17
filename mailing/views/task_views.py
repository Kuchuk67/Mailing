from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from ..models import ClientName, Message, Task, EmailForSend
from django.views.generic import ListView, DetailView
from ..forms import TaskForm



# Views for model Task


class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    paginate_by = 10
    template_name = 'mailing/tasks/task_list.html'
    extra_context = {"active_menu": "task"}

    def get_context_data(self):
        context = super().get_context_data()
        page = self.request.GET.get('page')
        context['page'] = page
        context['clients_counter'] = EmailForSend.objects.values('task_id').order_by('task_id').annotate(field_count=Count('task_id'))
        print(context['clients_counter'])
        return context


class TaskDetailsView(DetailView):
    model = Task
    context_object_name = 'task'
    extra_context = {"active_menu": "task"}


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('mailing:tasks')
    extra_context = {"active_menu": "task"}
    template_name = 'mailing/tasks/task_form.html'


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('mailing:tasks')
    extra_context = {"active_menu": "task"}
    template_name = 'mailing/tasks/task_form.html'


class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('mailing:tasks')
    extra_context = {"active_menu": "task"}
    template_name = 'mailing/tasks/task_confirm_delete.html'




