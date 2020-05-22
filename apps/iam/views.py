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
import re
import json
import datetime
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.views.generic import TemplateView, View
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count
from django.shortcuts import redirect
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from common.permissions import PermissionsMixin, IsValidUser
from common.http import HttpResponseTemporaryRedirect
from organization.utils import current_org
from assets.models import Asset
from access.models import StatisticsCredential


class IndexView(PermissionsMixin, TemplateView):
    template_name = 'index.html'
    permission_classes = [IsValidUser]

    session_month = None
    session_month_dates = []
    session_month_dates_archive = []

    @staticmethod
    def get_user_count():
        """
        获取所有用户
        :return: count
        """
        return current_org.get_org_members().count()

    @staticmethod
    def get_asset_count():
        """
        获取所有资产
        :return: count
        """
        return Asset.objects.all().count()

    @staticmethod
    def get_online_user_count():
        """
        获取在线用户
        :return: count
        """
        return len(set(Session.objects.filter(expire_date__gte=timezone.now())))

    def get_new_user_count_percentage(self):
        """
        获取最近30天新增用户占总用户的比例
        :return: count
        """
        recent = timezone.now() - datetime.timedelta(days=30)
        total = self.get_user_count()
        new = current_org.get_org_members().filter(date_joined__gte=recent).count()
        sums = new / total * 100
        return sums

    def get_new_asset_count_percentage(self):
        """
        获取最近30天新增资产占总资产的比例
        :return: count
        """
        recent = timezone.now() - datetime.timedelta(days=30)
        total = self.get_asset_count()
        new = Asset.objects.filter(date_created__gte=recent).count()
        sums = new / total * 100
        return sums

    def get_online_user_count_percentage(self):
        """
        获取在线用户占总用户的比例
        :return: count
        """
        total = self.get_user_count()
        new = self.get_online_user_count()
        sums = new / total * 100
        return sums

    def get_month_login_metrics(self):
        data = []
        time_min = datetime.datetime.min.time()
        time_max = datetime.datetime.max.time()
        for d in self.session_month_dates:
            ds = datetime.datetime.combine(d, time_min).replace(tzinfo=timezone.get_current_timezone())
            de = datetime.datetime.combine(d, time_max).replace(tzinfo=timezone.get_current_timezone())
            data.append(self.session_month.filter(date_start__range=(ds, de)).count())
        return data

    def get_month_active_user_total(self):
        return self.session_month.values('user').distinct().count()

    def get_credentials_type(self):
        credentials_type = StatisticsCredential.objects.values_list('credential_type', flat=True)

        credentials = []
        if 'amazon-iam-role' or 'amazon-access-key' in list(credentials_type):
            credentials.append(
                {
                    "label": "AWS",
                    "colors": "#ff9900",
                    "value": credentials_type.filter(credential_type__startswith='amazon').count()
                }
            )
        if 'google' in list(credentials_type):
            credentials.append(
                {
                    "label": "Google",
                    "colors": "#0aa858",
                    "value": credentials_type.filter(credential_type__startswith='google').count()
                }
            )
        if 'huawei' in list(credentials_type):
            credentials.append(
                {
                    "label": "HuaWei",
                    "colors": "#ff3333",
                    "value": credentials_type.filter(credential_type__startswith='huawei').count()
                }
            )
        if 'azure' in list(credentials_type):
            credentials.append(
                {
                    "label": "azure",
                    "colors": "#7460ee",
                    "value": credentials_type.filter(credential_type__startswith='azure').count()
                }
            )
        if 'aliyun' in list(credentials_type):
            credentials.append(
                {
                    "label": "Aliyun",
                    "colors": "#1976d2",
                    "value": credentials_type.filter(credential_type__startswith='Aliyun').count()
                }
            )
        if 'tencent' in list(credentials_type):
            credentials.append(
                {
                    "label": "tencent",
                    "colors": "#26c6da",
                    "value": credentials_type.filter(credential_type__startswith='tencent').count()
                }
            )

        return credentials

    def get_context_data(self, **kwargs):

        context = {
            'assets_count': self.get_asset_count(),
            'users_count': self.get_user_count(),
            'online_user_count': self.get_online_user_count(),
            # 'online_asset_count': self.get_online_session_count(),
            'new_user_count': self.get_new_user_count_percentage(),
            'new_asset_count': self.get_new_asset_count_percentage(),
            'online_user_percentage': self.get_online_user_count_percentage(),
            'month_total_visit_count': self.get_month_login_metrics(),
            'credentials_type': json.dumps(self.get_credentials_type()),
        }
        kwargs.update(context)
        return super(IndexView, self).get_context_data(**kwargs)


class I18NView(View):
    def get(self, request, lang):
        referer_url = request.META.get('HTTP_REFERER', '/')
        response = HttpResponseRedirect(referer_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
        return response
