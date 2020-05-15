#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: utils.py
@ide: PyCharm
@time: 2020/5/13 16:04
@desc:
"""
from datetime import datetime
from django.db.utils import IntegrityError
from common.utils import get_logger
from access.models import AmazonCredentialRole, AccessKeys
from ..handler import AWSConnector
from ..models import Asset, Tags

from common.utils import capital_to_lower

logger = get_logger(__file__)


def data_storage(access):

    for config in access:
        if config.credentials.credential_type == 'amazon-iam-role':
            try:
                access = AmazonCredentialRole.objects.get(pk=config.credentials.credential)

            except AmazonCredentialRole.DoesNotExist:
                logger.error('access credentials type matching query does not exist')
            else:
                # TODO: 使用跨账户时，先去获取临时的凭证
                ec = AWSConnector(
                    access_key=access.access_key_id, secret_key=access.secret_access_key,
                    region=config.region, org_id=access.org_id, created_by='System',
                    comment='obtain and created by the system at %s' % datetime.now()
                )
                asset_storage(ec.get_ec2_info())
        elif config.credentials.credential_type == 'amazon-access-key':
            try:
                access = AccessKeys.objects.get(pk=config.credentials.credential)
            except AccessKeys.DoesNotExist:
                logger.error('access credentials type matching query does not exist')
            else:
                ec = AWSConnector(
                    access_key=access.access_key_id, secret_key=access.secret_access_key,
                    region=config.region, org_id=access.org_id, created_by='System',
                    comment='obtain and created by the system at %s' % datetime.now()
                )
                asset_storage(ec.get_ec2_info())


def asset_storage(asset):
    for assets in asset:
        # 读取EC2的Tags并创建赋予资产
        tags_id = []
        if len(assets['tags']) > 1:
            # tags = dict(map(lambda tag: (tag['Key'], tag['Value']), assets['tags']))
            for tags in assets['tags']:
                tags.update(
                    {
                        'org_id': assets.get('org_id'),
                        'category': Tags.SYSTEM_CATEGORY,
                        'comment': assets.get('comment')
                    }
                )
                try:
                    # 创建Tags
                    key = Tags.objects.create(**capital_to_lower(tags))
                    # 获取创建好的tags主键
                    tags_id.append(Tags.objects.get(key=key))
                    logger.info("Tags created successfully")
                except IntegrityError:
                    # Tags存在就获取主键
                    tags_id.append(Tags.objects.get(key=tags['Key'], value=tags['Value']).id)
                    logger.warning("Tags already exists")
                    pass

        try:
            asset = Asset.objects.create(
                ip=assets['public_ip'], instance_id=assets['instance_id'], hostname=assets['hostname'],
                instance_type=assets['instance_type'], instance_state=assets['instance_state'],
                private_ip=assets['private_ip'], public_ip=assets['public_ip'],
                cpu_cores=assets['cpu_options'].get('CoreCount'),
                cpu_count=assets['cpu_options'].get('CoreCount'),
                org_id=assets['org_id'], comment=assets['comment']
            )
            asset.tags.add(*tags_id)
        except IntegrityError:
            logger.warning("Asset already exists")
            pass
