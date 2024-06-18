from django.core.exceptions import ValidationError
from django.forms import ModelForm, IntegerField, Widget, Textarea, ImageField, CharField, PasswordInput, TextInput, \
    Form, FileInput, FileField

from apps.users.models import User


class UserLoginForm(Form):
    username = CharField(max_length=28, widget=TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}
    ))
    password = CharField(max_length=28, widget=PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}
    ))


class UserRegisterForm(ModelForm):
    password1 = CharField(max_length=28, widget=PasswordInput(
        attrs={'id': 'password', 'type': 'password'}))
    password2 = CharField(max_length=28, widget=PasswordInput(
        attrs={'id': 'password', 'type': 'password'}))
    avatar = FileField(widget=FileInput(attrs={'class': 'form-control'}))

    def save(self, commit=True):
        user = super().save(commit)
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 == password2:
            user.set_password(password1)
            user.save()
        else:
            raise ValidationError("Passwords must be match")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-control"})

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'avatar', 'birth_date', 'slug')


class UserUpdateForm(ModelForm):
    class Meta:
        password1 = CharField(max_length=28, widget=PasswordInput(
            attrs={'id': 'password', 'type': 'password'}))
        password2 = CharField(max_length=28, widget=PasswordInput(
            attrs={'id': 'password', 'type': 'password'}))
        avatar = FileField(widget=FileInput(attrs={'class': 'form-control'}))

        def save(self, commit=True):
            user = super().save(commit)
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 == password2:
                user.set_password(password1)
                user.save()
            else:
                raise ValidationError("Passwords must be match")

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs.update({'class': "form-control"})

        class Meta:
            model = User
            fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'avatar', 'birth_date', 'slug')
