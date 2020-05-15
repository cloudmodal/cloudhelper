#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: gateway.py
@ide: PyCharm
@time: 2020/3/2 18:13
@desc:
"""
import json
import requests
from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from requests.exceptions import ConnectionError
from httpsig.requests_auth import HTTPSignatureAuth
from django.utils.translation import ugettext as _

from common.utils import get_logger
from common.send_email import send_error_notification_mail

logger = get_logger(__name__)


class ApiAuthentication:

    @staticmethod
    def requests_url():
        return settings.IAM_URL

    @staticmethod
    def access_key_id():
        return settings.IAM_ACCESS_KEY_ID

    @staticmethod
    def secret_access_key():
        return settings.IAM_SECRET_ACCESS_KEY

    @staticmethod
    def date_format():
        return '%a, %d %b %Y %H:%M:%S GMT'

    @staticmethod
    def signature_headers():
        return ['(request-target)', 'accept', 'date']

    @staticmethod
    def auth():
        auth = HTTPSignatureAuth(
            key_id=ApiAuthentication.access_key_id(), secret=ApiAuthentication.secret_access_key(),
            algorithm='hmac-sha256', headers=ApiAuthentication.signature_headers()
        )
        return auth

    @staticmethod
    def headers():
        headers = {
            'content-type': 'application/json',
            'Date': datetime.utcnow().strftime(ApiAuthentication.date_format()),
            'User-Agent': 'Django/2.2 (Python3.7) Gecko/20100101 Identity Management/v1.1.0'
        }
        return headers


def connect_logs_system(*args, **kwargs):
    if args:
        pass
    url = kwargs.get('url')
    email = settings.RECEIVE_ERROR_MAIL
    name = settings.RECEIVE_ERROR_MAIL_NAME

    try:
        data = json.dumps(kwargs, default=str, ensure_ascii=False)
        response = requests.post(
            url, data=data.encode('utf-8'),
            auth=ApiAuthentication.auth(),
            headers=ApiAuthentication.headers(), timeout=120
        )
    except ConnectionError as e:
        logger.error(e)
        subject = _('与LogInspect失去联系')
        if cache.get(url, None) is None:
            send_error_notification_mail(name, email, subject, e)
        cache.set(url, kwargs, timeout=600)

    except UnicodeEncodeError as e:
        logger.error(e)
        subject = _('统一码编码错误')
        if cache.get(url, None) is None:
            send_error_notification_mail(name, email, subject, e)
        cache.set(url, kwargs, timeout=600)

    else:
        if response.status_code != 201:
            subject = '日志写入不成功'
            if cache.get(url, None) is None:
                send_error_notification_mail(name, email, subject, f'日志无法写入，系统返回状态为：{response.status_code}')
            cache.set(url, kwargs, timeout=600)
            logger.error(f'日志无法写入，系统返回状态为：{response.status_code}')
        logger.debug('日志写入成功！')
