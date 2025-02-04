from django import forms
from .models import Task,Message,ClientName
from django.contrib.admin import helpers, widgets
from datetime import datetime
#import pytz


class TaskForm(forms.ModelForm):
    start_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'title':  'дата создания'},
                                          format='%Y-%m-%dT%H:%M'), label='Время начала рассылки'  )
    end_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'title':  'дата последнего изменения'},
                                                              format='%Y-%m-%dT%H:%M'), label='Время завершение рассылки')

    class Meta:
        model = Task
        input_formats = ['%Y-%m-%dT%H:%M:%SZ']
        fields = ['name',  'start_at', 'end_at', 'status', 'message']

    def clean(self):
        cleaned_data = super().clean()
        start_at = self.cleaned_data.get('start_at')
        end_at = self.cleaned_data.get('end_at')
        status = self.cleaned_data.get('status')

        if end_at <= start_at:
            self.add_error('end_at', 'Дата завершения должна быть позже даты начала')

        print(start_at.strftime('%Y-%m-%d %H:%M:%S'), str(datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")))
        if status == 'created' and start_at.strftime('%Y-%m-%d %H:%M:%S') < datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
            self.add_error('end_at', 'При запуске рассылки установите время начала больше текущего')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title_mail', 'text_mail']


class ClientNameForm(forms.ModelForm):
    class Meta:
        model = ClientName
        fields = ['email', 'name', 'description']


