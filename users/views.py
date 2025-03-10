from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import UpdateView


from .models import CustomUser
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from config import settings
from django.core.mail import send_mail
from .forms import SignUpForm, UserUpdateForm
import secrets
from config import settings
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse



# Create your views here.
class SignUpView(CreateView):
    model = CustomUser
    form_class = SignUpForm
    success_url = reverse_lazy('users:login')
    template_name ='register.html'


    @staticmethod
    def message_to(mail_to, token):
        send_mail(
            f"Регистрация в сервисе рассылок",
            f"""Вы зарегистрированы на сервисе рассылок
            Поддтвердите ваш e-mail перейди по ссылке
            <a href="{settings.BASE_HOSTS}/mailing/users/activate?token={token}">{settings.BASE_HOSTS}/mailing/users/activate?token={token}</a>
Ваш логин e-mail: {mail_to}""",
            settings.EMAIL_HOST_USER,
            (mail_to,),
            fail_silently=False,
        )

    def form_valid(self, form):
        token = secrets.token_urlsafe(20)
        self.message_to(self.request.POST.get('email'), token)
        form.instance.is_active = False
        form.instance.token_for_activate = token
        return super().form_valid(form)


def activate_user(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        user = CustomUser.objects.filter(token_for_activate=token).first()

        if user:
            user.is_active = True
            user.token_for_activate = ''

            user.save()
    return redirect('users:login')






class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    success_url = reverse_lazy('mailing:tasks')
    template_name = 'profile_edite.html'
    path_img_temp = None



    # Определяем текущего пользователя и грузим только его
    def get_object(self, queryset=None):
        """queryset = self.get_queryset()
        queryset = queryset.filter(pk=self.request.user.pk)
        return queryset.get()"""
        return self.request.user


    def get_success_url(self):
        return reverse('mailing:analitic')



