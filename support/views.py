# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from .models import Issue
from django.db.models import Q
from .forms import CreateIssueForm, RegisterForm, SearchIssueForm
from django.views import generic

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
    # TODO Редирект. Авторизованного на список, неавторизованного на создание обращения
    return render(request,"base.html",{'user': request.user})

@require_GET
@login_required
def my_issues(request):
    # TODO формы списка обращений не должно быть две. это одна форма
    if request.user.is_staff:
        HttpResponseRedirect(reverse("unresolved-issues"))
    issues = Issue.objects.filter(author = request.user.username)
    issues = issues.order_by('-creation_date')
    issues = paginate(request, issues)
    issues.paginator.baseurl = reverse("unresolved-issues")+'?page='
    context = {
        'issues': issues,
        'paginator': issues.paginator
    }
    return render(request, 'issues.html',context)

def get_base_url(params):
    if 'page' in params:
        params.pop('page')
    if params:
        baseurl = reverse("unresolved-issues")
        baseurl += '?' + params.urlencode()
        baseurl += '&page='
    else:
        baseurl = reverse("unresolved-issues")+'?page='
    return baseurl

def parse_search_params(params):
    issues = Issue.objects.all()
    show_closed = params.get('show_closed',None)
    if not (show_closed and show_closed == 'on'):
        issues = issues.filter(solved = False)
    author = params.get('author', None)
    if author:
        issues = issues.filter(Q(author__icontains = author) | Q(author_email__icontains = author))
    date = params.get('date', None)
    if date:
        issues = issues.filter(creation_date__date = date)
    return issues

@require_GET
@login_required
def unresolved_issues(request):
    issues = parse_search_params(request.GET)
    issues = issues.order_by('-creation_date')
    issues = paginate(request, issues)
    issues.paginator.baseurl = get_base_url(request.GET.copy())
    form = SearchIssueForm(initial = request.GET)
    context = {
        'issues': issues,
        'paginator': issues.paginator,
        'form': form
    }
    return render(request, 'issues.html',context)

@require_GET
def issue(request, issue_id):
    issue = get_object_or_404(Issue, id = issue_id)
    return render(request, 'issue.html',{'issue': issue})

class IssueView(generic.DetailView):
    model = Issue
    template_name = 'issue.html'

def create_issue(request):
    if request.method == "POST":
        form = CreateIssueForm(request.POST)
        if form.is_valid():
            issue = form.save()
            request.session['email'] = issue.author_email
            url = issue.get_absolute_url()
            return HttpResponseRedirect(url)
        else:
            render(request, 'create_issue.html', {'form': form})
    else:
        if request.user.is_authenticated():
            initial = {
                "author_email":request.user.email,
                "author": request.user.username
                }
        else:
            initial = {
                "author_email": request.session.get("email", "")}
        form = CreateIssueForm(initial = initial)
    return render(request, 'create_issue.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {
        'form': form,
    })

def logoutview(request):
    logout(request)
    return HttpResponseRedirect("/")
