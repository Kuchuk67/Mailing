from django import forms
from .models import Task
from django.contrib.admin import helpers, widgets
from datetime import datetime
# , 'min':datetime.now().strftime("%Y-%m-%dT%H:%M")

class NewDataForm(forms.ModelForm):
    start_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'},
                                        format='%Y-%m-%dT%H:%M'))
    end_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'},
                                                              format='%Y-%m-%dT%H:%M'))

    class Meta:
        model = Task
        input_formats = ['%Y-%m-%dT%H:%M:%SZ']
        fields = ['name', 'start_at', 'end_at', 'status', 'message',]