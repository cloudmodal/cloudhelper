#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: asset_sync.py
@ide: PyCharm
@time: 2020/5/13 16:01
@desc:
"""
from celery import shared_task

from ops.celery.utils import create_or_update_celery_periodic_tasks
from ops.celery.decorator import after_app_ready_start
from common.utils import get_logger
from ..models import AssetConfigs

from .utils import data_storage
from access.models import AmazonCredentialRole, AccessKeys
from ..handler import AWSConnector

logger = get_logger(__file__)


@shared_task
def assets_sync(asset_config=None):
    if asset_config:
        data_storage(asset_config)
    else:
        data_storage(AssetConfigs.objects.exclude(state=False))
    # for asset in config:
    #     print(asset.credentials.credential_type)
    #     print(asset.account)
    #
    #     data_storage(asset.credentials.credential_type, asset.region)
    #     if asset.credentials.credential_type == 'amazon-access-key':
    #         access = AccessKeys.objects.get(pk=asset.credentials.credential)
    #         ec = AWSConnector(
    #             access_key=access.access_key_id, secret_key=access.secret_access_key, region=asset.region
    #         )
    #         print(ec.get_ec2_info())
    #     if not user.is_valid:
    #         continue
    #     if not user.password_will_expired:
    #         continue
    #     send_password_expiration_reminder_mail(user)
    #     msg = "The user {} password expires in {} days"
    #     logger.info(msg.format(user, user.password_expired_remain_days))


@shared_task
@after_app_ready_start
def check_assets_sync_periodic():
    tasks = {
        'check_assets_sync_periodic': {
            'task': assets_sync.name,
            'interval': None,
            'crontab': '0 */6 * * *',
            'enabled': True,
        }
    }
    create_or_update_celery_periodic_tasks(tasks)
