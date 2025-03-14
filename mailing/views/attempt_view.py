from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from mailing.models import Attempt


class AttemptListView(LoginRequiredMixin, ListView):
    model = Attempt
    context_object_name = "attempts"
    template_name = "mailing/attempt/attempt_list.html"
    paginate_by = 15
    extra_context = {"active_menu": "attempt"}

    def get_queryset(self):
        return Attempt.objects.filter(task_send__user=self.request.user)
