from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import UpdateView

from ..forms import ModerationTaskForm
from ..models import CustomUser, EmailForSend, Task


class ModerationTaskListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "mailing.can_moderation_mailing"

    model = Task
    context_object_name = "tasks"
    paginate_by = 10
    template_name = "mailing/tasks/task_list_moderator.html"
    extra_context = {"active_menu": "moderation"}

    def post(self, request, *args, **kwargs):
        # деактивировать/активировать пользователя
        user_id = request.POST.get("user")
        user = CustomUser.objects.get(id=user_id)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()

        return redirect("mailing:moderation_tasks")

    # фильтр по пользователю
    def get_queryset(self):
        user_id = self.request.GET.get("user_id")
        if user_id:
            return Task.objects.filter(user=user_id)
        return Task.objects.all()

    def get_context_data(self):
        context = super().get_context_data()
        page = self.request.GET.get("page")
        context["page"] = page
        context["clients_counter"] = (
            EmailForSend.objects.values("task_id")
            .order_by("task_id")
            .annotate(field_count=Count("task_id"))
        )
        print(context["tasks"])
        # context['user_activ'] =    CustomUser.objects.values('username')
        return context


class ModerationTaskUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "mailing.can_moderation_mailing"
    model = Task
    form_class = ModerationTaskForm
    success_url = reverse_lazy("mailing:moderation_tasks")
    extra_context = {"active_menu": "moderation"}
    template_name = "mailing/tasks/task_form_moderator.html"

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(ModerationTaskUpdateView, self).get_form_kwargs()
        form_kwargs["initial"] = {"user_pk": self.request.user.pk}
        return form_kwargs


class ModerationUserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "users.can_moderation_users"
    model = CustomUser
    context_object_name = "users"
    paginate_by = 10
    template_name = "mailing/users/user_list_moderator.html"
    extra_context = {"active_menu": "users"}

    def post(self, request, *args, **kwargs):
        # деактивировать/активировать пользователя
        user_id = request.POST.get("user")
        user = CustomUser.objects.get(id=user_id)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()

        return redirect("mailing:moderation_users")
