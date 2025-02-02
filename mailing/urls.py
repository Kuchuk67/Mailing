
from django.urls import path
from mailing import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'mailing'

urlpatterns = [
    # Получатели рассылки - Клиенты
    path('client/', views.ClientNameListView.as_view(), name='clients'),
    #path('client/<int:pk>', views.ClientNameDetailsView.as_view(), name='client_details'),
    path('client/create', views.ClientNameCreateView.as_view(), name='client_create'),
    path('client/<int:pk>', views.ClientNameUpdateView.as_view(), name='client_edit'),
    path('client/<int:pk>/delete', views.ClientNameDeleteView.as_view(), name='client_delete'),

    # Отписка от рассылок
    path('unsubscribe/', views.UnsubscribeDetailView.as_view(), name='unsubscribe'),

    # Тексты сообщений для рассылок
    path('message/', views.MessageListView.as_view(), name='messages'),
    path('message/create', views.MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>', views.MessageUpdateView.as_view(), name='message_edit'),
    path('message/<int:pk>/delete', views.MessageDeleteView.as_view(), name='message_delete'),

    # Планирование рассылок - Задачи
    path('task/', views.TaskListView.as_view(), name='tasks'),
    path('task/create', views.TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>', views.TaskUpdateView.as_view(), name='task_edit'),
    path('task/<int:pk>/delete', views.TaskDeleteView.as_view(), name='task_delete'),

    path('', views.ClientNameListView.as_view(), name='clients'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)