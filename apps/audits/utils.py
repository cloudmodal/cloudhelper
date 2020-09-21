#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: utils.py
@ide: PyCharm
@time: 2020/3/2 11:33
@desc:
"""
import csv
import codecs
from django.http import HttpResponse
from django.utils.translation import ugettext as _

from common.utils import (
    validate_ip, get_ip_city, get_logger
)

logger = get_logger(__name__)


def get_resource_type_list():
    from account.models import User, UserGroup
    from assets.models import (
        Asset, Tags, AssetConfigs, AdminUser, SystemUser, CommandFilter,
        CommandFilterRule,
    )
    from organization.models import Organization

    models = [
        User, UserGroup, Asset, Tags, AdminUser, SystemUser,
        AssetConfigs, Organization, CommandFilter, CommandFilterRule
    ]
    return [model._meta.verbose_name for model in models]


def get_excel_response(filename):
    excel_response = HttpResponse(content_type='text/csv')
    excel_response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    excel_response.write(codecs.BOM_UTF8)
    return excel_response


def write_content_to_excel(response, header=None, login_logs=None, fields=None):
    writer = csv.writer(response, dialect='excel', quoting=csv.QUOTE_MINIMAL)
    if header:
        writer.writerow(header)
    if login_logs:
        for log in login_logs:
            data = [getattr(log, field.name) for field in fields]
            writer.writerow(data)
    return response


def write_login_log(*args, **kwargs):
    default_city = _("Unknown")
    ip = kwargs.get('ip') or ''
    if not (ip and validate_ip(ip)):
        ip = ip[:15]
        city = default_city
    else:
        city = get_ip_city(ip) or default_city
    if kwargs.get('type') is None or kwargs.get('type') == '':
        login_type = 'T'
    else:
        login_type = kwargs.get('type')
    # url = settings.LOG_CORE_HOST + '/v1/logs/login/'
    kwargs.update({'ip': ip, 'city': city, 'type': login_type, 'logs_type': 'login_log'})
    # connect_logs_system(*args, **kwargs)
    send_sqs(*args, **kwargs)


def write_operate_logs(**kwargs):
    # url = settings.LOG_CORE_HOST + '/v1/logs/operate/'
    kwargs.update({'logs_type': 'operate_logs'})
    # connect_logs_system(**kwargs)
    send_sqs(**kwargs)


def write_password_change_log(**kwargs):
    # url = settings.LOG_CORE_HOST + '/v1/logs/password/'
    kwargs.update({'logs_type': 'password_change_log'})
    # connect_logs_system(**kwargs)
    send_sqs(**kwargs)


def send_sqs(*args, **kwargs):
    if args:
        print(args)

    parameters = kwargs
    from common.queue import InspectQueue
    sqs = InspectQueue()
    sqs.send(parameters)
