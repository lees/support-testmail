# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime
from django.core.mail import send_mail

example = [
	{
		"creation_date": datetime.now(),
		'solved': True,
		"solved_date": datetime.now(),
		'solved_by': "support1",
		'subject': "Ничего не работает",
		'text': "Ну вообще ничего",
		"author": "vasya_pupkin",
		"email": "vasya_cool@mail.ru"
	},
	{
		"creation_date": datetime.now(),
		'solved': True,
		"solved_date": datetime.now(),
		'solved_by': "support2",
		'subject': "Ничего не работает 2",
		'text': "Ну вообще ничего, кроме саппорта",
		"author": "vasya_kupkin",
		"email": "vasya_cool1@mail.ru"
	},
	]

@require_GET
def root(request):
    return render(request,"base.html",{'user': request.user})

@require_GET
@login_required
def my_issues(request):
	#TODO pagination
	return render(request, 'issues.html',{'issues': example})

@require_GET
def unresolved_issues(request):
	#TODO pagination
	return render(request, 'issues.html',{'issues': example})

@require_GET
def issue(request, issue_id):
	return render(request, 'issue.html',{'issue': example[0], 'id': issue_id})

def create_issue(request):
	#TODO mail-from from config
	send_mail('subj', 'message', 'from@support.mail', ['to@user.ru'], fail_silently = True)
	return HttpResponse('create_issue')
