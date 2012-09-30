# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from websites.models import get_url_informations
from websites.forms import SuggestForm
from uxperiment.utils import send_message

@csrf_protect
@login_required
def suggest(request):
    """ Suggest form
    Display and proceed suggest a website form submission
    """
    if request.method == 'POST':
        form = SuggestForm(request.POST)
        if form.is_valid():
            website = form.save()
            data = {'website': website.url, 'username': request.user.username,
                    'sender': request.user.email}
            send_message('suggest', data)
            return HttpResponseRedirect(reverse('confirm_suggest_website'))
    else:
        form = SuggestForm()
    return render(request, 'websites/suggest.html', {'form': form})

def confirm_suggest(request):
    """ Suggest form confirmation """
    return render(request, 'websites/confirm_suggest.html')

def informations(request):
    """ Get informations about a website """
    if request.is_ajax():
        success = False
        infos = { 'error': u'Requête invalide' }
        if 'GET' == request.method:
            success, infos = get_url_informations(request.GET['url'])

            if success:
                status=200
            else:
                status=409

        return HttpResponse(json.dumps(infos),
            content_type="application/json", status=status)
    else:
        raise Http404
