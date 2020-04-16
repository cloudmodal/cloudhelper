#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: api.py
@ide: PyCharm
@time: 2020/2/5 20:22
@desc:
"""
import json
from django.http import HttpResponse
from rest_framework.views import APIView
from django.utils.translation import ugettext_lazy as _
from rest_framework.permissions import AllowAny


class IndexAPI(APIView):
    """首页"""
    permission_classes = (AllowAny,)
    success_message = _("OK")

    @staticmethod
    def get(request):
        content = {'code': 200, 'msg': 'OK'}
        content = json.dumps(content)
        response = HttpResponse(content=content, content_type='application/json')
        response.status_code = 200
        return response

    @staticmethod
    def post(request):
        content = {'code': 200, 'msg': "OK"}
        content = json.dumps(content)
        response = HttpResponse(content=content, content_type='application/json')
        response.status_code = 200
        return response
