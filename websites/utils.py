# -*- coding: utf-8 -*-

from django.forms import URLField
from django.utils.translation import ugettext as _

from models import Website

from bs4 import BeautifulSoup
import requests

import re


def get_url_informations(url):
    """Get informations about a url"""

    error_invalid = False, {'error': _(u'Invalid URL')}
    error_exist = False, {'error': _(u'This URL has already been submitted')}
    error_connect = False, {'error': _(u'Failed at opening the URL')}

    # Check url is valid
    try:
        url_field = URLField()
        clean_url = url_field.clean(url)
    except:
        return error_invalid

    # Check url exist
    if exist_url(clean_url):
        return error_exist

    # Get informations
    req = requests.get(clean_url)
    if req.status_code == 200:
        final_url = req.url
        soup = BeautifulSoup(req.text)
        title = soup.title.string
        description = soup.findAll('meta',
            attrs={'name': re.compile("^description$", re.I)})[0].get('content')
    else:
        return error_connect

    # Check final url exist if different from clean url
    if final_url != clean_url:
        if exist_url(final_url):
            return error_exist

    return True, {
        'url': final_url,
        'title': title,
        'description': description,
    }


def exist_url(url):
    """Check url exist"""
    return Website.objects.filter(url__exact=url).exists()
