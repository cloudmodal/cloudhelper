#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: group.py
@ide: PyCharm
@time: 2020/4/20 19:00
@desc:
"""
from django.utils.translation import ugettext as _
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin

from common.utils import get_logger
from common.const import create_success_msg, update_success_msg
from common.permissions import PermissionsMixin, IsOrgAdmin
from organization.utils import current_org
from ..models import UserGroup
from .. import forms

__all__ = ['UserGroupListView', 'UserGroupCreateView', 'UserGroupDetailView',
           'UserGroupUpdateView', 'UserGroupGrantedAssetView']
logger = get_logger(__name__)


class UserGroupListView(PermissionsMixin, TemplateView):
    template_name = 'group/user_group_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Users'),
            'action': _('User group list')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserGroupCreateView(PermissionsMixin, SuccessMessageMixin, CreateView):
    model = UserGroup
    form_class = forms.UserGroupForm
    template_name = 'group/user_group_create_update.html'
    success_url = reverse_lazy('users:user-group-list')
    success_message = create_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Users'),
            'action': _('Create user group'),
            'type': 'create'
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserGroupUpdateView(PermissionsMixin, SuccessMessageMixin, UpdateView):
    model = UserGroup
    form_class = forms.UserGroupForm
    template_name = 'group/user_group_create_update.html'
    success_url = reverse_lazy('users:user-group-list')
    success_message = update_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Users'),
            'action': _('Update user group'),
            'type': 'update'

        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserGroupDetailView(PermissionsMixin, DetailView):
    model = UserGroup
    context_object_name = 'user_group'
    template_name = 'group/user_group_detail.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        users = current_org.get_org_members(exclude=('Auditor',)).exclude(
            groups=self.object)
        context = {
            'app': _('Users'),
            'action': _('User group detail'),
            'users': users,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserGroupGrantedAssetView(PermissionsMixin, DetailView):
    model = UserGroup
    template_name = 'group/user_group_granted_asset.html'
    context_object_name = 'user_group'
    object = None
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Users'),
            'action': _('User group granted asset'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
