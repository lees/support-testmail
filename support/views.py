# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from .models import Issue

def paginate(request, qs):
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(qs, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page

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
	issues = Issue.objects.filter(solved = False)
	issues = paginate(request, issues)
	issues.paginator.baseurl = reverse("unresolved-issues")+'?page='
	context = {
		'issues': issues,
		'paginator': issues.paginator
	}
	return render(request, 'issues.html',context)

@require_GET
def issue(request, issue_id):
	issue = get_object_or_404(Issue, id = issue_id)
	return render(request, 'issue.html',{'issue': issue})

def create_issue(request):
	#TODO mail-from from config
	send_mail('subj', 'message', 'from@support.mail', ['to@user.ru'], fail_silently = True)
	return HttpResponse('create_issue')
