
from django.urls import path
from mailing import views

app_name = 'mailing'

urlpatterns = [
    # Получатели рассылки - Клиенты
    path('mailing/client/', views.ClientNameListView.as_view(), name='clients'),
    path('mailing/client/<int:pk>', views.ClientNameListView.as_view(), name='client_details'),
    path('mailing/client/<int:pk>/edit', views.ClientNameListView.as_view(), name='client_edit'),
    path('mailing/client/<int:pk>/delete', views.ClientNameListView.as_view(), name='client_delete'),

    # Отписка от рассылок
    path('mailing/unsubscribe/', views.UnsubscribeDetailView.as_view(), name='unsubscribe'),

    # Тексты сообщений для рассылок
    path('mailing/message/', views.MessageListView.as_view(), name='messages'),
    path('mailing/message/<int:pk>', views.MessageListView.as_view(), name='message_details'),
    path('mailing/message/<int:pk>/edit', views.MessageListView.as_view(), name='message_edit'),
    path('mailing/message/<int:pk>/delete', views.MessageListView.as_view(), name='message_delete'),

    # Планирование рассылок - Задачи
    path('mailing/task/', views.TaskListView.as_view(), name='tasks'),
    path('mailing/task/<int:pk>', views.TaskListView.as_view(), name='task_details'),
    path('mailing/task/<int:pk>/edit', views.TaskListView.as_view(), name='task_edit'),
    path('mailing/task/<int:pk>/delete', views.TaskListView.as_view(), name='task_delete'),




]

