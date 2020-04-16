#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: errors.py
@ide: PyCharm
@time: 2019/12/20 12:15
@desc:
"""
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.conf import settings

from .signals import post_auth_failed
from account.utils import (
    increase_login_failed_count, get_login_failed_count
)

reason_password_failed = 'password_failed'
reason_code_failed = 'code_failed'
reason_mfa_failed = 'mfa_failed'
reason_user_not_exist = 'user_not_exist'
reason_password_expired = 'password_expired'
reason_user_invalid = 'user_invalid'
reason_user_inactive = 'user_inactive'

reason_choices = {
    reason_code_failed: _('验证码错误'),
    reason_password_failed: _('用户名和/或密码不正确'),
    reason_mfa_failed: _('MFA authentication failed'),
    reason_user_not_exist: _("用户不存在"),
    reason_password_expired: _("密码已过期"),
    reason_user_invalid: _('禁用或过期'),
    reason_user_inactive: _("这个账号未激活")
}
old_reason_choices = {
    '0': '-',
    '1': reason_choices[reason_password_failed],
    '2': reason_choices[reason_mfa_failed],
    '3': reason_choices[reason_user_not_exist],
    '4': reason_choices[reason_password_expired],
}

session_empty_msg = _("No session found, check your cookie")
invalid_login_msg = _(
    "登录失败, 用户名或密码错误，注意：您还可以尝试{times_try}次，(超过{times_try}次该账户将被锁定{block_time}分钟！)"
)
block_login_msg = _(
    "该帐户已被锁定(请与管理员联系以将其解锁，或在{}分钟后重试)"
)
mfa_failed_msg = _("MFA code invalid, or ntp sync server time")

mfa_required_msg = _("MFA required")
login_confirm_required_msg = _("需要登录确认")
login_confirm_wait_msg = _("Wait login confirm ticket for accept")
login_confirm_error_msg = _("Login confirm ticket was {}")


class AuthFailedNeedLogMixin:
    username = ''
    request = None
    error = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        post_auth_failed.send(
            sender=self.__class__, username=self.username,
            request=self.request, reason=self.error
        )


class AuthFailedNeedBlockMixin:
    username = ''
    ip = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        increase_login_failed_count(self.username, self.ip)


class AuthFailedError(Exception):
    status = None
    username = ''
    msg = ''
    error = ''
    error_code = None
    request = None
    ip = ''

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def as_data(self):
        return {
            "status": self.status,
            "error_code": self.error_code,
            "error": self.error,
            "msg": self.msg,
        }


class CredentialError(AuthFailedNeedLogMixin, AuthFailedNeedBlockMixin, AuthFailedError):
    def __init__(self, error, username, ip, request, status=None, error_code=None):
        super().__init__(
            error=error, username=username, ip=ip,
            status=status, error_code=error_code, request=request
        )
        times_up = settings.SECURITY_LOGIN_LIMIT_COUNT
        times_failed = get_login_failed_count(username, ip)
        times_try = int(times_up) - int(times_failed)
        block_time = settings.SECURITY_LOGIN_LIMIT_TIME

        default_msg = invalid_login_msg.format(
            times_try=times_try, block_time=block_time
        )
        if error == reason_password_failed:
            self.msg = default_msg
            self.status = 400
            self.error_code = 40001
        else:
            self.msg = reason_choices.get(error, default_msg)
            self.status = 400
            self.error_code = 40000


class MFAFailedError(AuthFailedNeedLogMixin, AuthFailedError):
    error = reason_mfa_failed
    msg = mfa_failed_msg

    def __init__(self, username, request):
        super().__init__(username=username, request=request)


class BlockLoginError(AuthFailedNeedBlockMixin, AuthFailedError):
    error = 'block_login'
    msg = block_login_msg.format(settings.SECURITY_LOGIN_LIMIT_TIME)

    def __init__(self, username, ip):
        super().__init__(username=username, ip=ip)


class SessionEmptyError(AuthFailedError):
    msg = session_empty_msg
    error = 'session_empty'


class NeedMoreInfoError(Exception):
    error = ''
    msg = ''

    def __init__(self, error='', msg=''):
        if error:
            self.error = error
        if msg:
            self.msg = msg

    def as_data(self):
        return {
            'error': self.error,
            'msg': self.msg,
        }


class MFARequiredError(NeedMoreInfoError):
    msg = mfa_required_msg
    error = 'mfa_required'

    def as_data(self):
        return {
            'error': self.error,
            'msg': self.msg,
            'data': {
                'choices': ['otp'],
                'url': reverse('api-auth:mfa-challenge')
            }
        }


class LoginConfirmBaseError(NeedMoreInfoError):
    def __init__(self, ticket_id, **kwargs):
        self.ticket_id = ticket_id
        super().__init__(**kwargs)

    def as_data(self):
        return {
            "error": self.error,
            "msg": self.msg,
            "data": {
                "ticket_id": self.ticket_id
            }
        }


class LoginConfirmWaitError(LoginConfirmBaseError):
    msg = login_confirm_wait_msg
    error = 'login_confirm_wait'


class LoginConfirmOtherError(LoginConfirmBaseError):
    error = 'login_confirm_error'

    def __init__(self, ticket_id, status):
        msg = login_confirm_error_msg.format(status)
        super().__init__(ticket_id=ticket_id, msg=msg)
