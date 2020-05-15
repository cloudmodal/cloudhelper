#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: runtime_config.py
@ide: PyCharm
@time: 2020/2/16 14:08
@desc:
"""
import os
from django.conf import settings


class RuntimeConfig:

    DEFAULTS = {
        'boto3_retries': 1,
        'role_arn': None,
        'role_external_id': None,
        'china': 'cn-north-1',
        'standard': 'us-east-1',
        'inspect_sqs_queue_url': settings.INSPECT_SQS_QUEUE_URL,
        'inspect_sqs_queue_wait_period': 0,
    }

    @classmethod
    def get_conf_value(cls, key: str, resource_tags=None, lambda_payload=None):
        # priority 3 are resource tags
        if resource_tags is not None:
            tag_key = f"l2c:config:{key}"
            if tag_key in resource_tags:
                return resource_tags[tag_key]

        # priority 2 is lambda payload
        if (lambda_payload is not None) and ('config' in lambda_payload) and (key in lambda_payload['config']):
            return lambda_payload['config'][key]

        # priority 1 are environment variables
        if key in os.environ:
            return os.environ[key]

        # priority 0 are defaults
        if key in cls.DEFAULTS:
            return cls.DEFAULTS[key]

    @classmethod
    def get_envvalue(cls, key: str, default_value):
        return os.environ[key] if key in os.environ else default_value

    @classmethod
    def boto3_retry_times(cls):
        return cls.get_conf_value('boto3_retries', None, None)

    @classmethod
    def get_role_arn(cls, engine):
        return cls.get_conf_value('role_arn', None, engine.lambda_payload)

    @classmethod
    def get_role_external_id(cls, engine):
        return cls.get_conf_value('role_external_id', None, engine.lambda_payload)

    @classmethod
    def get_china_defaults_region(cls):
        return cls.get_conf_value('china', None, None)

    @classmethod
    def get_standard_defaults_region(cls):
        return cls.get_conf_value('standard', None, None)

    @classmethod
    def get_sqs_queue_url(cls, engine):
        return cls.get_conf_value('inspect_sqs_queue_url', None, engine.lambda_payload)

    @classmethod
    def get_sqs_queue_wait_period(cls, engine):
        return cls.get_conf_value('inspect_sqs_queue_wait_period', None, engine.lambda_payload)
