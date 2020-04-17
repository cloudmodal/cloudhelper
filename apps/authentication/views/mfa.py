#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: mfa.py
@ide: PyCharm
@time: 2020/4/16 23:29
@desc:
"""
from django.views.generic.edit import FormView
from .. import forms, errors, mixins
from .utils import redirect_to_guard_view

__all__ = ['UserLoginOtpView']


class UserLoginOtpView(mixins.AuthMixin, FormView):
    template_name = 'authentication/login_otp.html'
    form_class = forms.UserCheckOtpCodeForm
    redirect_field_name = 'next'

    def form_valid(self, form):
        otp_code = form.cleaned_data.get('otp_code')
        try:
            self.check_user_mfa(otp_code)
            return redirect_to_guard_view()
        except errors.MFAFailedError as e:
            form.add_error('otp_code', e.msg)
            return super().form_invalid(form)
