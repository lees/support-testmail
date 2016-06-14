# -*- coding: utf-8 -*-

from django import forms
from .models import Issue
from django.contrib.auth.models import User
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings


class CreateIssueForm(forms.Form):
    author_email = forms.EmailField(
            label=u'Электронный адрес для оповещения',
            max_length=100,
            required=False)
    author = forms.IntegerField(widget=forms.HiddenInput, required=False)
    subject = forms.CharField(
                label='Тема',
                max_length=255,
                widget=forms.TextInput(attrs={'size': 80}))
    text = forms.CharField(
            label="Текст",
            widget=forms.Textarea(attrs={'cols': 80}))

    def clean_author(self):
        author = self.cleaned_data.get("author", None)
        if not author:
            return None
        try:
            author = User.objects.get(id=author)
        except User.DoesNotExist:
            return None
        return author

    def clean(self):
        if self.cleaned_data.get('author', None):
            return
        if self.cleaned_data.get('author_email', None):
            return
        raise forms.ValidationError(
                u'Должен быть заполнен адрес уведомления',
                code="email_empty")

    def save(self):
        post = Issue(**self.cleaned_data)
        post.clean()
        post.save()
        return post


class PostAnswerForm(forms.Form):
    issue_id = forms.DecimalField(widget=forms.HiddenInput)
    solved_by = forms.IntegerField(widget=forms.HiddenInput)
    response_text = forms.CharField(
            label='Текст ответа',
            widget=forms.Textarea(attrs = {'cols':80}))

    def clean_solved_by(self):
        solved_by = self.cleaned_data.get("solved_by", None)
        if not solved_by:
            text = u'Невозможно определить сотрудника, давшего ответ'
            raise forms.ValidationError(text, code="empty_solved_by")
        try:
            solved_by = User.objects.get(id=solved_by)
        except User.DoesNotExist:
            return None
        return solved_by

    def save(self):
        issue_id = self.cleaned_data.get('issue_id', None)
        if not issue_id:
            return
        try:
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            return
        issue.solved_by = self.cleaned_data.get('solved_by')
        issue.response_text = self.cleaned_data.get('response_text')
        issue.solved = True
        issue.solved_date = datetime.now()
        issue.save()

        # TODO Обработать ошибку отправки почты (сделать очередь заданий)
        # TODO Взять почту из пользователя?
        subject = u"Получен ответ на ваше обращение: %s " % issue.subject
        send_mail(
            subject,
            issue.response_text,
            settings.FROM_EMAIL,
            [issue.author_email],
            fail_silently=False)
        return issue


class SearchIssueForm(forms.Form):
    date = forms.DateField(label=u"Дата обращения")
    author = forms.CharField(label=u"Автор обращения", max_length=255)
    show_closed = forms.BooleanField(label=u"Показывать завершенные")


class RegisterForm(forms.Form):
    name = forms.CharField(label="Имя полльзователя", max_length=100)
    email = forms.EmailField(label="Адрес электронной почты", max_length=100)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            text = u'Пользователь с таким email уже существует'
            error = forms.ValidationError(text, code="email_exist")
            self.add_error('email', error)
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            text = u'Пароль должен состоять минимум из 8 символов'
            error = forms.ValidationError(text, code="short_password")
            self.add_error('password', error)
        return password

    def clean(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            text = u'Пароль и подтверждение пароля должны совпадать'
            error = forms.ValidationError(text, code="passwords_differ")
            self.add_error('password', error)

    def save(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.create_user(name, email, password)
        return user
