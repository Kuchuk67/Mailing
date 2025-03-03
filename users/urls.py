from django.urls import path
from users.views import SignUpView, activate_user
from django.contrib.auth.views import LoginView, LogoutView



app_name = 'users'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name = "login.html"), name='login'),
    path('logout/', LogoutView.as_view(next_page = 'mailing:messages'), name='logout'),
    path('activate/', activate_user)
    #path('profile/', ProfileUpdateView.as_view(), name='profile'),
    #path('profile/', ProfileDetailView.as_view(), name='profile'),
    #path('profile/edite/', ProfileUpdateView.as_view(), name='profile_edite'),
]