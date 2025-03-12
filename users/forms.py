from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
import re


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        """Обновление стилей формы обновления"""
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )

    # Проверка уникальности полей
    def clean_email(self):
        email = self.cleaned_data["email"]
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой e-mail уже существует")
        return email


class UserUpdateForm(forms.ModelForm):
    """
    Форма обновления данных пользователя
    """

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы обновления
        """
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )
        # self.fields['email'].widget.attrs.update({'class': 'form-control', })
        self.fields["country"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )
        self.fields["phone"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )

    class Meta:
        model = CustomUser
        fields = ["username", "country", "phone"]

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        phone = "".join(re.findall("[0-9]", phone))
        if len(phone) < 8:
            raise forms.ValidationError("Номер телефона должен содержать минимум 8 цифр")
        return phone
