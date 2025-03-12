from django import forms
from .models import Task, Message, ClientName
from datetime import datetime


class TaskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        print("*****", kwargs.get("initial").get("user_pk"))
        user_pk = kwargs.get("initial").get("user_pk")
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields["message"].queryset = Message.objects.filter(user=user_pk)

    start_at = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"class": "form-control", "type": "datetime-local", "title": "дата создания"},
            format="%Y-%m-%dT%H:%M",
        ),
        label="Время начала рассылки",
    )
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}), label="Комментарий")

    class Meta:
        model = Task
        input_formats = ["%Y-%m-%dT%H:%M:%SZ"]
        fields = ["name", "start_at", "status", "message", "description"]
        # exclude = ['user']

    def clean(self):
        super().clean()
        start_at = self.cleaned_data.get("start_at")
        status = self.cleaned_data.get("status")
        if status == "created" and start_at.strftime("%Y-%m-%d %H:%M:%S") < datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ):
            self.add_error("start_at", "При запуске рассылки установите время начала больше текущего")


class ModerationTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        input_formats = ["%Y-%m-%dT%H:%M:%SZ"]
        fields = ["status"]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["title_mail", "text_mail"]


class ClientNameForm(forms.ModelForm):
    class Meta:
        model = ClientName
        fields = ["email", "name", "description"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.user = kwargs["initial"].get("user")
        super(ClientNameForm, self).__init__(*args, **kwargs)

    def clean(self):
        # проверка дублирующего ключа
        email = self.cleaned_data.get("email")
        qs = ClientName.objects.filter(email=email, user=self.user)
        if qs:
            self.add_error("email", "Такой email уже есть в базе")


class DeleteObjectForm(forms.ModelForm):
    class Meta:
        model = ClientName
        fields = []
