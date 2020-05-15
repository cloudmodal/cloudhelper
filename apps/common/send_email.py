#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: send_email.py
@ide: PyCharm
@time: 2020/1/14 12:09
@desc:
"""
import logging
from datetime import datetime
from django.conf import settings
from django.template import loader
from django.utils.translation import ugettext as _

from common.utils import reverse
from common.tasks import send_ses_email


logger = logging.getLogger('iam')


def construct_user_created_email_body(user):
    """构造用户创建的电子邮件正文"""
    default_body = _("""
        <div>
            <p>您的帐户已成功创建</p>
            <div>
                用户: %(username)s
                <br/>
                设置密码: <a href="%(rest_password_url)s?token=%(rest_password_token)s">点击这里设置您的密码</a> 
                (此链接有效期为1个小时。 过期后, <a href="%(forget_password_url)s?email=%(email)s">重新请求</a>)
            </div>
            <div>
                <p>---</p>
                <a href="%(login_url)s">直接登录</a>
            </div>
        </div>
        """) % {
        'username': user.name,
        'rest_password_url': settings.REST_PASSWORD_URL,
        'rest_password_token': user.generate_reset_token(),
        'forget_password_url': settings.FORGET_PASSWORD_URL,
        'email': user.email,
        'login_url': settings.LOGIN_URL,
    }

    if settings.EMAIL_CUSTOM_USER_CREATED_BODY:
        custom_body = '<p style="text-indent:2em">' + settings.EMAIL_CUSTOM_USER_CREATED_BODY + '</p>'
    else:
        custom_body = ''
    body = custom_body + default_body
    return body


def send_user_code_mail(email, code):
    """发送电子邮件验证码"""
    recipient_list = email
    subject = _('Security Code')
    signature = settings.EMAIL_CUSTOM_USER_CREATED_SIGNATURE
    message = loader.render_to_string(
        'mail/send_user_code.html',
        {
            'subject': subject,
            'recipient': email,
            'signature': signature,
            'code': code
        }
    )
    if settings.DEBUG:
        try:
            print(message)
        except OSError:
            logger.debug('OS Error')

    send_ses_email.delay(RECIPIENT=recipient_list, SUBJECT=subject, BODY_TEXT=message, BODY_HTML=message)


def send_user_created_mail(user):
    recipient_list = user.email
    subject = _('Create account successfully')
    if settings.EMAIL_CUSTOM_USER_CREATED_SUBJECT:
        subject = settings.EMAIL_CUSTOM_USER_CREATED_SUBJECT

    message = loader.render_to_string(
        'mail/user_created_mail.html',
        {
            'user': user,
        }
    )
    if settings.DEBUG:
        try:
            print(message)
        except OSError:
            logger.debug('OS Error')

    send_ses_email.delay(RECIPIENT=recipient_list, SUBJECT=subject, BODY_TEXT=message, BODY_HTML=message)


def send_user_registered_mail(user):
    recipient_list = user.email
    subject = _('Create account successfully')
    if settings.EMAIL_CUSTOM_USER_CREATED_SUBJECT:
        subject = settings.EMAIL_CUSTOM_USER_CREATED_SUBJECT

    message = loader.render_to_string(
        'mail/user_registered_mail.html',
        {
            'user': user,
            'confirm_verification': reverse('account:confirm-verification', kwargs={
                'token': user.generate_reset_token()
            }, external=True),
        }
    )
    if settings.DEBUG:
        try:
            print(message)
        except OSError:
            logger.debug('OS Error')

    send_ses_email.delay(RECIPIENT=recipient_list, SUBJECT=subject, BODY_TEXT=message, BODY_HTML=message)


def send_reset_password_mail(user):
    subject = _('Reset password')
    recipient_list = user.email
    message = loader.render_to_string(
        'mail/reset_password_mail.html',
        {
            'name': user.name,
            'rest_password_url': "reverse('users:reset-password', external=True)",
            'rest_password_token': 'user.generate_reset_token()',
            'forget_password_url': "reverse('users:forgot-password', external=True)",
            'email': user.email,
            'login_url': "reverse('authentication:login', external=True)",
        }
    )
    if settings.DEBUG:
        logger.debug(message)

    send_ses_email.delay(RECIPIENT=recipient_list, SUBJECT=subject, BODY_TEXT=message, BODY_HTML=message)


def send_password_expiration_reminder_mail(user):
    subject = _('Security notice')
    recipient_list = user.email
    message = loader.render_to_string(
        'mail/send_password_expiration_reminder_mail.html',
        {
            'name': user.name,
            'date_password_expired': datetime.fromtimestamp(datetime.timestamp(
                user.date_password_expired)).strftime('%Y-%m-%d %H:%M'),
            'update_password_url': reverse('users:user-password-update', external=True),
            'forget_password_url': reverse('users:forgot-password', external=True),
            'email': user.email,
            'login_url': reverse('authentication:login', external=True),
        }
    )
    if settings.DEBUG:
        logger.debug(message)

    send_ses_email.delay(RECIPIENT=recipient_list, SUBJECT=subject, BODY_TEXT=message, BODY_HTML=message)


def send_user_expiration_reminder_mail(user):
    subject = _('Expiration notice')
    recipient_list = user.email
    message = loader.render_to_string(
        '',
        {
            'name': user.name,
            'date_expired': datetime.fromtimestamp(datetime.timestamp(
                user.date_expired)).strftime('%Y-%m-%d %H:%M'),
        }
    )
    if settings.DEBUG:
        logger.debug(message)

    send_ses_email.delay(RECIPIENT=recipient_list, SUBJECT=subject, BODY_TEXT=message, BODY_HTML=message)


def send_reset_ssh_key_mail(user):
    subject = _('SSH Key Reset')
    recipient_list = user.email
    message = loader.render_to_string(
        'mail/send_reset_ssh_key_mail.html',
        {
            'name': user.name,
            'login_url': reverse('authentication:login', external=True),
        }
    )
    if settings.DEBUG:
        logger.debug(message)

    send_ses_email.delay(RECIPIENT=recipient_list, SUBJECT=subject, BODY_TEXT=message, BODY_HTML=message)


def send_error_notification_mail(name, email, subject, message):
    message = loader.render_to_string(
        'mail/send_error_notification_mail.html',
        {
            'name': name,
            'message': message
        }
    )
    if settings.DEBUG:
        logger.debug(message)

    send_ses_email.delay(RECIPIENT=email, SUBJECT=subject, BODY_TEXT=message, BODY_HTML=message)
