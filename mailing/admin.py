from django.contrib import admin

from mailing.models import ClientName, Message, Task
from mailing.views import TaskListView


# Register your models here.

@admin.register(ClientName)
class ClientNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title_mail', 'created_at', 'updated_at',)
    search_fields = ('title_mail', 'created_at', 'updated_at',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_at', 'end_at', 'status',)
    search_fields = ('name', )
    list_filter = ( 'status', 'start_at', 'end_at',)


