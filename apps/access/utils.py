#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: utils.py
@ide: PyCharm
@time: 2020/2/14 16:05
@desc:
"""
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache

from common.utils import get_logger
from common.utils import generate_random_string
from .models import StatisticsCredential


logger = get_logger(__file__)

# see Issue #222
now_localtime = getattr(timezone, 'template_localtime', timezone.localtime)


def now():
    """Return the current date and time."""
    if getattr(settings, 'USE_TZ', False):
        return now_localtime(timezone.now())
    else:
        return timezone.now()


def create_or_update_credential(tasks):
    for name, detail in tasks.items():
        defaults = dict(
            org_id=detail.get('org_id'),
            credential=detail.get('credential'),
            credentials_name=detail.get('credentials_name'),
            account_type=detail.get('account_type'),
            credential_type=detail.get('credential_type'),
            date_created=detail.get('date_created'),
            date_updated=detail.get('date_updated'),
            created_by=detail.get('created_by')
        )
        task = StatisticsCredential.objects.update_or_create(
            defaults=defaults, name=name,
        )
        return task


def delete_credential_relevance(task_name):
    StatisticsCredential.objects.filter(name=task_name).delete()


def cross_accounts(user):
    if settings.CHINA_REQUIRE_EXTERNAL_ID:
        china = 'china-' + user
        china_external_id = settings.CHINA_EXTERNAL_ID + '-' + generate_random_string(8)
        if cache.get(china, None) is None:
            cache.set(china, china_external_id, timeout=60 * 3)
            cache_china_external_id = cache.get(china, None)
        else:
            cache_china_external_id = cache.get(china, None)
    else:
        cache_china_external_id = ''

    if settings.GLOBAL_REQUIRE_EXTERNAL_ID:
        key = 'global-' + user
        global_external_id = settings.GLOBAL_EXTERNAL_ID + '-' + generate_random_string(8)
        if cache.get(key, None) is None:
            cache.set(key, global_external_id, timeout=60 * 3)
            cache_global_external_id = cache.get(key, None)
        else:
            cache_global_external_id = cache.get(key, None)
    else:
        cache_global_external_id = ''

    accounts = [
        {
            'region': 'Amazon China',
            'AccountID': settings.CHINA_ACCOUNT_ID,
            'RequireExternalID': settings.CHINA_REQUIRE_EXTERNAL_ID,
            'ExternalID': cache_china_external_id,
            'RequireMFA': settings.CHINA_REQUIRE_MFA,
        },
        {
            'region': 'Amazon Global',
            'AccountID': settings.GLOBAL_ACCOUNT_ID,
            'RequireExternalID': settings.GLOBAL_REQUIRE_EXTERNAL_ID,
            'ExternalID': cache_global_external_id,
            'RequireMFA': settings.GLOBAL_REQUIRE_MFA,
        }
    ]
    return accounts
