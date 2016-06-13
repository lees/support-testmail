# -*- coding: utf-8 -*-

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from .models import Issue
from django.contrib.auth.models import User
from .forms import CreateIssueForm, RegisterForm, SearchIssueForm, PostAnswerForm
from django.views import generic

@require_GET
def root(request):
    #return render(request,"base.html",{'user': request.user})
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('create-issue'))
    return HttpResponseRedirect(reverse('issues'))


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

def get_base_url(params):
    if 'page' in params:
        params.pop('page')
    if params:
        baseurl = reverse("issues")
        baseurl += '?' + params.urlencode()
        baseurl += '&page='
    else:
        baseurl = reverse("issues")+'?page='
    return baseurl

def parse_search_params(params):
    issues = Issue.objects.all()
    show_closed = params.get('show_closed',None)
    if show_closed != 'on':
        issues = issues.filter(solved = False)
    author = params.get('author', None)
    if author:
        users = User.objects.filter(username__contains = author)
        issues = issues.filter(author__in = users)
    date = params.get('date', None)
    if date:
        issues = issues.filter(creation_date__date = date)
    return issues

@require_GET
@login_required
def issues(request):
    if request.user.is_staff:
        issues = parse_search_params(request.GET)
    else:
        issues = Issue.objects.filter(author = request.user)
    issues = issues.order_by('-creation_date')
    issues = paginate(request, issues)
    issues.paginator.baseurl = get_base_url(request.GET.copy())
    print(request.GET.copy())
    form = SearchIssueForm(initial = request.GET)
    context = {
        'issues': issues,
        'paginator': issues.paginator,
        'form': form
    }
    return render(request, 'issues.html',context)

@require_GET
@login_required
def issue(request, pk):
    issue = get_object_or_404(Issue, id = pk)
    if not request.user.is_staff and request.user != issue.author:
        raise PermissionDenied
    form = PostAnswerForm( initial = {'issue_id': pk, 'solved_by': request.user.pk})
    return render(request, 'issue.html',{'issue': issue, 'form': form})

@require_GET
@login_required
def account(request, pk):
    try:
        pk = int(pk)
    except ValueError:
        raise Http404
    if not request.user.is_staff and request.user.pk != pk:
        raise PermissionDenied
    user = get_object_or_404(User, id = pk)
    issues = Issue.objects.filter(author = user).count()
    return render(request, 'user_profile.html',{'user_profile': user, 'issues': issues})

@require_POST
@login_required
def response_issue(request):
    if not request.user.is_staff:
        raise PermissionDenied
    form = PostAnswerForm(request.POST)
    if form.is_valid():
        issue = form.save()
        if issue:
            return HttpResponseRedirect(issue.get_absolute_url())
    return HttpResponseRedirect('/')

def create_issue(request):
    if request.method == "POST":
        form = CreateIssueForm(request.POST)
        print(form.errors)
        if form.is_valid():
            issue = form.save()
            # Сохраняем почту в сессии, чтобы в следующий раз не нужно было ее заполнять
            request.session['email'] = issue.author_email
            return HttpResponseRedirect(reverse("issue-created"))
        else:
            render(request, 'create_issue.html', {'form': form})
    else:
        if request.user.is_authenticated():
            initial = {
                "author_email":request.user.email,
                "author": request.user.pk
                }
        else:
            initial = {
                "author_email": request.session.get("email", "")}
        print(initial)
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

def issue_created(request):
    return render(request, "issue_created.html")
