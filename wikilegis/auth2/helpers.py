# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from urlparse import urlparse, urlunparse
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import QueryDict
from django.shortcuts import resolve_url
from wikilegis.helpers import nocontext


@nocontext
def login_absolute_path(request, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    path = request.build_absolute_uri()
    resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
    # If the login url is the same scheme and net location then just
    # use the path as the "next" url.
    login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
    current_scheme, current_netloc = urlparse(path)[:2]
    if ((not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)):
        path = request.get_full_path()

    resolved_url = resolve_url(login_url or settings.LOGIN_URL)

    login_url_parts = list(urlparse(resolved_url))
    if redirect_field_name:
        querystring = QueryDict(login_url_parts[4], mutable=True)
        querystring[redirect_field_name] = path
        login_url_parts[4] = querystring.urlencode(safe='/')

    return urlunparse(login_url_parts)
