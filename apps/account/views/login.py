#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: login.py
@ide: PyCharm
@time: 2020/4/17 16:06
@desc:
"""
from django.shortcuts import render
from django.views.generic import RedirectView, UpdateView
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, redirect
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView
from django.conf import settings
from django.urls import reverse_lazy
from formtools.wizard.views import SessionWizardView

from common.utils import get_object_or_none
from common import send_email
from common.permissions import PermissionsMixin, IsValidUser
from ..models import User
from ..utils import (
    get_password_check_rules, check_password_rules
)
from .. import forms

__all__ = [
    'UserLoginView', 'UserForgotPasswordSendmailSuccessView',
    'UserResetPasswordSuccessView', 'UserResetPasswordSuccessView',
    'UserResetPasswordView', 'UserForgotPasswordView', 'UserFirstLoginView',
]


class UserLoginView(RedirectView):
    url = reverse_lazy('authentication:login')
    query_string = True


class UserForgotPasswordView(TemplateView):
    template_name = 'account/forgot_password.html'

    def post(self, request):
        email = request.POST.get('email')
        user = get_object_or_none(User, email=email)
        if not user:
            error = _('Email address invalid, please input again')
            return self.get(request, errors=error)
        elif not user.can_update_password():
            error = _('User auth from {}, go there change password'.format(user.source))
            return self.get(request, errors=error)
        else:
            send_email.send_reset_password_mail(user)
            return HttpResponseRedirect(
                reverse('account:forgot-password-sendmail-success'))


class UserForgotPasswordSendmailSuccessView(TemplateView):
    template_name = 'flash_message_standalone.html'

    def get_context_data(self, **kwargs):
        context = {
            'title': _('Send reset password message'),
            'messages': _('Send reset password mail success, '
                          'login your mail box and follow it '),
            'redirect_url': reverse('authentication:login'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserResetPasswordSuccessView(TemplateView):
    template_name = 'flash_message_standalone.html'

    def get_context_data(self, **kwargs):
        context = {
            'title': _('Reset password success'),
            'messages': _('Reset password success, return to login page'),
            'redirect_url': reverse('authentication:login'),
            'auto_redirect': True,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserResetPasswordView(TemplateView):
    template_name = 'account/reset_password.html'

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token', '')
        user = User.validate_reset_password_token(token)
        if not user:
            kwargs.update({'errors': _('Token invalid or expired')})
        else:
            check_rules = get_password_check_rules()
            kwargs.update({'password_check_rules': check_rules})
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        password = request.POST.get('password')
        password_confirm = request.POST.get('password-confirm')
        token = request.GET.get('token')

        if password != password_confirm:
            return self.get(request, errors=_('Password not same'))

        user = User.validate_reset_password_token(token)
        if not user:
            return self.get(request, errors=_('Token invalid or expired'))
        if not user.can_update_password():
            error = _('User auth from {}, go there change password'.format(user.source))
            return self.get(request, errors=error)

        is_ok = check_password_rules(password)
        if not is_ok:
            return self.get(
                request,
                errors=_('* Your password does not meet the requirements')
            )

        user.reset_password(password)
        User.expired_reset_password_token(token)
        return HttpResponseRedirect(reverse('account:reset-password-success'))


class UserFirstLoginView(PermissionsMixin, UpdateView):
    """用户首次登录成功后，完善个人信息视图"""
    model = User
    permission_classes = [IsValidUser]
    form_class = forms.UserFirstLoginForm
    template_name = 'account/first_login.html'
    success_url = reverse_lazy('account:user-profile')

    def get_object(self, queryset=None):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_first_login:
            return redirect(reverse('index'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'app': _('User'),
            'action': _('First login'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        choices = form.cleaned_data.get('mfa_level')
        # 强制启用后用户无法手动关闭
        if self.request.user.mfa_force_enabled:
            user.is_first_login = False
        else:
            user.mfa_level = choices
            user.is_first_login = False
        user.save()
        return super().form_valid(form)
