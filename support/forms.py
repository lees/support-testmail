# -*- coding: utf-8 -*-

from django import forms
from .models import Issue
from django.contrib.auth.models import User

class CreateIssueForm(forms.Form):
    author_email = forms.EmailField(max_length=100)
    subject = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)

    def save(self):
        post = Issue(**self.cleaned_data)
        post.save()
        return post

class RegisterForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError(u'Пользователь с таким email уже существует', code = "email_exist")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            error = forms.ValidationError(u'Пароль должен состоять минимум из 8 символов', code = "short_password")
            self.add_error('password', error)
            return password
        return password

    def clean(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError(u'Пароль и подтверждение пароля не совпадают', code = "passwords_differ")

    def save(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.create_user(name, email, password)
        return user
