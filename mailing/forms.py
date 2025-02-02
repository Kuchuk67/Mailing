from django import forms
from .models import Task
from django.contrib.admin import helpers, widgets

class NewDataForm(forms.ModelForm):
    #start_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'value': '2013-07-12T07:00:00Z+03','type': 'datetime-local'}))
    #end_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'value': '03.02.2025T19:32','type': 'datetime-local'}))

    start_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'},
                                        format='%Y-%m-%dT%H:%M'))
    end_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'},
                                                              format='%Y-%m-%dT%H:%M'))

    class Meta:
        model = Task
        input_formats = ['%Y-%m-%dT%H:%M:%SZ']
        fields = ['name', 'start_at', 'end_at', 'status', 'message',]


class EventSplitDateTime(widgets.AdminSplitDateTime):
    def __init__(self, attrs=None):
        # Вызываем метод базового класса
        super().__init__(attrs)


class EventForm(forms.ModelForm):
    start_at = forms.DateTimeField(
        widget=EventSplitDateTime() ) #SplitDateTimeWidget( ) )#date_attrs={ 'type': 'date'},time_attrs={ 'type': 'time'})
    end_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={ 'type': 'datetime-local'}))

    class Meta:
        model = Task
        input_formats = ['%Y-%m-%dT%H:%M:%SZ']
        fields = ['name', 'start_at', 'end_at', 'status', 'message', ]