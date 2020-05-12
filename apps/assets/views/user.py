#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: user.py
@ide: PyCharm
@time: 2020/5/8 16:55
@desc:
"""
from django.utils.translation import ugettext as _
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import DetailView, SingleObjectMixin

from common.const import create_success_msg, update_success_msg
from .. import forms
from ..models import AdminUser, SystemUser, CommandFilter
from common.permissions import PermissionsMixin, IsOrgAdmin

__all__ = [
    'AdminUserCreateView', 'AdminUserDetailView',
    'AdminUserDeleteView', 'AdminUserListView',
    'AdminUserUpdateView', 'AdminUserAssetsView',
    'SystemUserCreateView', 'SystemUserUpdateView',
    'SystemUserDetailView', 'SystemUserDeleteView',
    'SystemUserAssetView', 'SystemUserListView',
]


class AdminUserListView(PermissionsMixin, TemplateView):
    model = AdminUser
    template_name = 'assets/admin_user_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Admin user list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AdminUserCreateView(PermissionsMixin, SuccessMessageMixin, CreateView):
    model = AdminUser
    form_class = forms.AdminUserForm
    template_name = 'assets/admin_user_create_update.html'
    success_url = reverse_lazy('assets:admin-user-list')
    success_message = create_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Create admin user'),
            "type": "create"
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AdminUserUpdateView(PermissionsMixin, SuccessMessageMixin, UpdateView):
    model = AdminUser
    form_class = forms.AdminUserForm
    template_name = 'assets/admin_user_create_update.html'
    success_url = reverse_lazy('assets:admin-user-list')
    success_message = update_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Update admin user'),
            "type": "update"
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AdminUserDetailView(PermissionsMixin, DetailView):
    model = AdminUser
    template_name = 'assets/admin_user_detail.html'
    context_object_name = 'admin_user'
    object = None
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Admin user detail'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AdminUserAssetsView(PermissionsMixin, SingleObjectMixin, ListView):
    paginate_by = settings.DISPLAY_PER_PAGE
    template_name = 'assets/admin_user_assets.html'
    context_object_name = 'admin_user'
    object = None
    permission_classes = [IsOrgAdmin]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=AdminUser.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = self.object.assets.all()
        return self.queryset

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Admin user detail'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AdminUserDeleteView(PermissionsMixin, DeleteView):
    model = AdminUser
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('assets:admin-user-list')
    permission_classes = [IsOrgAdmin]


class SystemUserListView(PermissionsMixin, TemplateView):
    template_name = 'assets/system_user_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('System user list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class SystemUserCreateView(PermissionsMixin, SuccessMessageMixin, CreateView):
    model = SystemUser
    form_class = forms.SystemUserForm
    template_name = 'assets/system_user_create.html'
    success_url = reverse_lazy('assets:system-user-list')
    success_message = create_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Create system user'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class SystemUserUpdateView(PermissionsMixin, SuccessMessageMixin, UpdateView):
    model = SystemUser
    form_class = forms.SystemUserForm
    template_name = 'assets/system_user_update.html'
    success_url = reverse_lazy('assets:system-user-list')
    success_message = update_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Update system user')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class SystemUserDetailView(PermissionsMixin, DetailView):
    template_name = 'assets/system_user_detail.html'
    context_object_name = 'system_user'
    model = SystemUser
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        cmd_filters_remain = CommandFilter.objects.exclude(system_users=self.object)
        context = {
            'app': _('Assets'),
            'action': _('System user detail'),
            'cmd_filters_remain': cmd_filters_remain,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class SystemUserDeleteView(PermissionsMixin, DeleteView):
    model = SystemUser
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('assets:system-user-list')
    permission_classes = [IsOrgAdmin]


class SystemUserAssetView(PermissionsMixin, DetailView):
    model = SystemUser
    template_name = 'assets/system_user_assets.html'
    context_object_name = 'system_user'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('assets'),
            'action': _('System user asset'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
