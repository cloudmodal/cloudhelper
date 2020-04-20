#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: views.py
@ide: PyCharm
@time: 2020/4/17 15:39
@desc:
"""
import datetime
import re
import time

from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.views.generic import TemplateView, View
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count
from django.shortcuts import redirect
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from common.permissions import PermissionsMixin, IsValidUser
from common.http import HttpResponseTemporaryRedirect


class IndexView(PermissionsMixin, TemplateView):
    template_name = 'index.html'
    permission_classes = [IsValidUser]

    def get_context_data(self, **kwargs):
        context = {}
        kwargs.update(context)
        return super(IndexView, self).get_context_data(**kwargs)


class I18NView(View):
    def get(self, request, lang):
        referer_url = request.META.get('HTTP_REFERER', '/')
        response = HttpResponseRedirect(referer_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
        return response
