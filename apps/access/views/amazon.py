#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: amazon.py
@ide: PyCharm
@time: 2020/4/23 22:46
@desc:
"""

from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin

from common.utils import get_logger
from common.const import create_success_message, update_success_message
from common.permissions import PermissionsMixin, IsValidUser
from .. import models
from .. import forms

__all__ = [
    'CredentialsListView', 'CredentialsCreateView', 'CredentialsDetailView',
    'AmazonAccessKeyCreateView', 'AmazonRoleCreateView',
    'AmazonRoleUpdateView', 'AmazonAccessKeyUpdateView'

]
logger = get_logger(__name__)


class CredentialsListView(PermissionsMixin, TemplateView):
    template_name = 'access/credentials_list.html'
    permission_classes = [IsValidUser]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Credentials'),
            'action': _('Credentials list')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class CredentialsCreateView(PermissionsMixin, TemplateView):
    template_name = 'access/credentials_create.html'
    permission_classes = [IsValidUser]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Credentials'),
            'action': _('Create credentials'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class CredentialsDetailView(PermissionsMixin, DetailView):
    model = models.StatisticsCredential
    template_name = 'access/credentials_detail.html'
    context_object_name = "cred_object"
    key_prefix_block = "_LOGIN_BLOCK_{}"
    permission_classes = [IsValidUser]

    def get_context_data(self, **kwargs):
        pk = self.get_object().credential
        if self.get_object().credential_type == 'amazon-access-key':
            credentials = get_object_or_404(models.AccessKeys, pk=pk)
        elif self.get_object().credential_type == 'amazon-iam-role':
            credentials = get_object_or_404(models.AmazonCredentialRole, pk=pk)
        else:
            credentials = None
        context = {
            'app': _('Credentials'),
            'action': _('Credentials detail'),
            'credentials': credentials,
            'secret_access_key': '*****************************************'
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AmazonAccessKeyCreateView(PermissionsMixin, SuccessMessageMixin, CreateView):
    form_class = forms.AmazonAccessKeyCreateForm
    template_name = 'access/amazon_access_key_create.html'
    success_url = reverse_lazy('credentials:credentials-list')
    success_message = create_success_message

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Credentials'),
            'action': _('Register Amazon Access Key'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user = self.request.user
        user.credential_type = 'amazon-access-key'
        user.created_by = self.request.user.username or 'System'
        user.save()

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AmazonAccessKeyCreateView, self).get_form_kwargs()
        data = {'request': self.request}
        kwargs.update(data)
        return kwargs


class AmazonAccessKeyUpdateView(PermissionsMixin, SuccessMessageMixin, UpdateView):
    model = models.AccessKeys
    form_class = forms.AmazonAccessKeyUpdateForm
    template_name = 'access/amazon_access_key_update.html'
    context_object_name = 'cred_object'
    success_url = reverse_lazy('credentials:credentials-list')
    success_message = update_success_message
    permission_classes = [IsValidUser]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Credentials'),
            'action': _('Update Amazon IAM Role'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super(AmazonAccessKeyUpdateView, self).get_form_kwargs()
        data = {'request': self.request}
        kwargs.update(data)
        return kwargs


class AmazonRoleCreateView(PermissionsMixin, SuccessMessageMixin, CreateView):
    form_class = forms.AmazonRoleCreate
    template_name = 'access/amazon_iam_role_create.html'
    success_url = reverse_lazy('credentials:credentials-list')
    success_message = create_success_message

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Credentials'),
            'action': _('Register Amazon IAM Role'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user = self.request.user
        user.credential_type = 'amazon-iam-role'
        user.created_by = self.request.user.username or 'System'
        user.save()

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AmazonRoleCreateView, self).get_form_kwargs()
        data = {'request': self.request}
        kwargs.update(data)
        return kwargs


class AmazonRoleUpdateView(PermissionsMixin, SuccessMessageMixin, UpdateView):
    model = models.AmazonCredentialRole
    form_class = forms.AmazonRoleUpdate
    template_name = 'access/amazon_iam_role_update.html'
    context_object_name = 'cred_object'
    success_url = reverse_lazy('credentials:credentials-list')
    success_message = update_success_message
    permission_classes = [IsValidUser]

    def _deny_permission(self):
        obj = self.get_object()
        return not self.request.user.is_superuser and obj.is_superuser

    # def get(self, request, *args, **kwargs):
    #     if self._deny_permission():
    #         return redirect(self.success_url)
    #     return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Credentials'),
            'action': _('Update Amazon IAM Role'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super(AmazonRoleUpdateView, self).get_form_kwargs()
        data = {'request': self.request}
        kwargs.update(data)
        return kwargs
