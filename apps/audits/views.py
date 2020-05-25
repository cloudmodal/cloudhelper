#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: views.py
@ide: PyCharm
@time: 2020/5/25 13:13
@desc:
"""
import json
import uuid
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.utils.translation import ugettext as _
from django.db.models import Q

from audits.utils import get_excel_response, write_content_to_excel
from common.mixins import DatetimeSearchMixin
from common.permissions import (
    PermissionsMixin, IsOrgAdmin, IsValidUser, IsOrgAuditor
)
from organization.utils import current_org
# from ops.views import CommandExecutionListView as UserCommandExecutionListView
from .models import OperateLog, PasswordLog, LoginLog
from .utils import get_resource_type_list


class OperateLogListView(PermissionsMixin, DatetimeSearchMixin, ListView):
    model = OperateLog
    template_name = 'audit/operate_log_list.html'
    paginate_by = settings.DISPLAY_PER_PAGE
    user = action = resource_type = ''
    date_from = date_to = None
    actions_dict = dict(OperateLog.ACTION_CHOICES)
    permission_classes = [IsOrgAdmin | IsOrgAuditor]

    def get_queryset(self):
        self.queryset = super().get_queryset()
        self.user = self.request.GET.get('user')
        self.action = self.request.GET.get('action')
        self.resource_type = self.request.GET.get('resource_type')

        filter_kwargs = dict()
        filter_kwargs['datetime__gt'] = self.date_from
        filter_kwargs['datetime__lt'] = self.date_to
        if self.user:
            filter_kwargs['user'] = self.user
        if self.action:
            filter_kwargs['action'] = self.action
        if self.resource_type:
            filter_kwargs['resource_type'] = self.resource_type
        if filter_kwargs:
            self.queryset = self.queryset.filter(**filter_kwargs).order_by('-datetime')
        return self.queryset

    def get_context_data(self, **kwargs):
        context = {
            'user_list': current_org.get_org_members(),
            'actions': self.actions_dict,
            'resource_type_list': get_resource_type_list(),
            'date_from': self.date_from,
            'date_to': self.date_to,
            'user': self.user,
            'resource_type': self.resource_type,
            "app": _("Audits"),
            "action": _("Operate log"),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class PasswordLogList(PermissionsMixin, DatetimeSearchMixin, ListView):
    model = PasswordLog
    template_name = 'audit/password_log_list.html'
    paginate_by = settings.DISPLAY_PER_PAGE
    user = ''
    date_from = date_to = None
    permission_classes = [IsOrgAdmin | IsOrgAuditor]

    def get_queryset(self):
        users = current_org.get_org_members()
        self.queryset = super().get_queryset().filter(
            user__in=[user.__str__() for user in users]
        )
        self.user = self.request.GET.get('user')

        filter_kwargs = dict()
        filter_kwargs['datetime__gt'] = self.date_from
        filter_kwargs['datetime__lt'] = self.date_to
        if self.user:
            filter_kwargs['user'] = self.user
        if filter_kwargs:
            self.queryset = self.queryset.filter(**filter_kwargs).order_by('-datetime')
        return self.queryset

    def get_context_data(self, **kwargs):
        context = {
            'user_list': current_org.get_org_members(),
            'date_from': self.date_from,
            'date_to': self.date_to,
            'user': self.user,
            "app": _("Audits"),
            "action": _("Password change log"),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class LoginLogListView(PermissionsMixin, DatetimeSearchMixin, ListView):
    template_name = 'audit/login_log_list.html'
    model = LoginLog
    paginate_by = settings.DISPLAY_PER_PAGE
    user = keyword = ""
    date_to = date_from = None
    permission_classes = [IsOrgAdmin | IsOrgAuditor]

    @staticmethod
    def get_org_members():
        users = current_org.get_org_members().values_list('username', flat=True)
        return users

    def get_queryset(self):
        if current_org.is_default():
            queryset = super().get_queryset()
        else:
            users = self.get_org_members()
            queryset = super().get_queryset().filter(username__in=users)

        self.user = self.request.GET.get('user', '')
        self.keyword = self.request.GET.get("keyword", '')

        queryset = queryset.filter(
            datetime__gt=self.date_from, datetime__lt=self.date_to
        )
        if self.user:
            queryset = queryset.filter(username=self.user)
        if self.keyword:
            queryset = queryset.filter(
                Q(ip__contains=self.keyword) |
                Q(city__contains=self.keyword) |
                Q(username__contains=self.keyword)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Audits'),
            'action': _('Login log'),
            'date_from': self.date_from,
            'date_to': self.date_to,
            'user': self.user,
            'keyword': self.keyword,
            'user_list': self.get_org_members(),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


# class CommandExecutionListView(UserCommandExecutionListView):
#     user_id = None
#
#     @staticmethod
#     def get_user_list():
#         users = current_org.get_org_members(exclude=('Auditor',))
#         return users
#
#     def get_queryset(self):
#         queryset = self._get_queryset()
#         self.user_id = self.request.GET.get('user')
#         org_users = self.get_user_list()
#         if self.user_id:
#             queryset = queryset.filter(user=self.user_id)
#         else:
#             queryset = queryset.filter(user__in=org_users)
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'app': _('Audits'),
#             'action': _('Command execution log'),
#             'date_from': self.date_from,
#             'date_to': self.date_to,
#             'user_list': self.get_user_list(),
#             'keyword': self.keyword,
#             'user_id': self.user_id,
#         })
#         return context


@method_decorator(csrf_exempt, name='dispatch')
class LoginLogExportView(PermissionsMixin, View):
    permission_classes = [IsValidUser]

    def get(self, request):
        fields = [
            field for field in LoginLog._meta.fields
        ]
        filename = 'login-logs-{}.csv'.format(
            timezone.localtime(timezone.now()).strftime('%Y-%m-%d_%H-%M-%S')
        )
        excel_response = get_excel_response(filename)
        header = [field.verbose_name for field in fields]
        login_logs = cache.get(self.request.GET.get('spm', ''), [])

        response = write_content_to_excel(
            excel_response, login_logs=login_logs, header=header, fields=fields
        )
        return response

    def post(self, request):
        try:
            date_from = json.loads(self.request.body).get('date_from', [])
            date_to = json.loads(self.request.body).get('date_to', [])
            user = json.loads(self.request.body).get('user', [])
            keyword = json.loads(self.request.body).get('keyword', [])

            login_logs = LoginLog.get_login_logs(
                date_from=date_from, date_to=date_to, user=user,
                keyword=keyword,
            )
        except ValueError:
            return HttpResponse('Json object not valid', status=400)
        spm = uuid.uuid4().hex
        cache.set(spm, login_logs, 300)
        url = reverse('audits:login-log-export') + '?spm=%s' % spm
        return JsonResponse({'redirect': url})
