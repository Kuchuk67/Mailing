from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from ..models import ClientName, Message, Task
from django.views.generic import ListView, DetailView
from ..forms import NewDataForm, EventForm



# Views for model Task


class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    paginate_by = 25
    template_name = 'mailing/tasks/task_list.html'
    extra_context = {"active_menu": "task"}


class TaskDetailsView(DetailView):
    model = Task
    context_object_name = 'task'
    extra_context = {"active_menu": "task"}


class TaskCreateView(CreateView):
    model = Task
    form_class = NewDataForm
    #fields = ['name', 'start_at', 'end_at', 'status', 'message']
    success_url = reverse_lazy('mailing:tasks')
    extra_context = {"active_menu": "task"}
    template_name = 'mailing/tasks/task_form.html'


class TaskUpdateView(UpdateView):
    model = Task
    form_class = NewDataForm # EventForm
    #fields = ['name', 'start_at', 'end_at', 'status', 'message',]
    success_url = reverse_lazy('mailing:tasks')
    extra_context = {"active_menu": "task"}
    template_name = 'mailing/tasks/task_form.html'


class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('mailing:tasks')
    extra_context = {"active_menu": "task"}
    template_name = 'mailing/tasks/task_confirm_delete.html'
