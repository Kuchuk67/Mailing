
from django.urls import path
from mailing import views

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
    path('message/<int:pk>', views.MessageListView.as_view(), name='message_details'),
    path('message/<int:pk>/edit', views.MessageListView.as_view(), name='message_edit'),
    path('message/<int:pk>/delete', views.MessageListView.as_view(), name='message_delete'),

    # Планирование рассылок - Задачи
    path('task/', views.TaskListView.as_view(), name='tasks'),
    path('task/<int:pk>', views.TaskListView.as_view(), name='task_details'),
    path('task/<int:pk>/edit', views.TaskListView.as_view(), name='task_edit'),
    path('task/<int:pk>/delete', views.TaskListView.as_view(), name='task_delete'),




]

