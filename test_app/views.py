# -*- coding: utf-8 -*-

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
#from ..support.models import Issues

@require_GET
def root(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('create-issue'))
    return HttpResponseRedirect(reverse('issues'))


@require_GET
@login_required
def account(request, pk):
    try:
        pk = int(pk)
    except ValueError:
        raise Http404
    if not request.user.is_staff and request.user.pk != pk:
        raise PermissionDenied
    user = get_object_or_404(User, id=pk)
    # TODO fix or delete
    #issues = Issue.objects.filter(author=user).count()
    issues = 0
    context = {'user_profile': user, 'issues': issues}
    return render(request, 'support/user_profile.html', context)


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
