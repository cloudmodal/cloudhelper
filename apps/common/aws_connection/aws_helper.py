#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: aws_helper.py
@ide: PyCharm
@time: 2020/2/16 13:40
@desc:
"""
import boto3
from botocore.config import Config
from .runtime_config import RuntimeConfig


class AwsHelper:

    @staticmethod
    def local_account_id():
        return AwsHelper.boto3_client('sts').get_caller_identity()['Account']

    @staticmethod
    def local_region():
        return boto3.session.Session().region_name

    @staticmethod
    def boto3_retry_config():
        return RuntimeConfig.boto3_retry_times()

    @staticmethod
    def boto3_china_region():
        return RuntimeConfig.get_china_defaults_region()

    @staticmethod
    def boto3_standard_region():
        return RuntimeConfig.get_standard_defaults_region()

    @staticmethod
    def boto3_sts(arn, role_session_name, external_id):
        sts_client = boto3.client(
            'sts', config=Config(retries={'max_attempts': AwsHelper.boto3_retry_config()})
        )
        if external_id is not None:
            assumed_role_object = sts_client.assume_role(
                RoleArn=arn, ExternalId=external_id,
                RoleSessionName=role_session_name,
            )
        else:
            assumed_role_object = sts_client.assume_role(
                RoleArn=arn, RoleSessionName=role_session_name
            )

        return assumed_role_object

    @staticmethod
    def boto3_client(service_name, region_name=None, arn=None, role_session_name=None, external_id=None):
        if region_name is None:
            region_name = AwsHelper.local_region()

        if arn is not None:
            credentials = AwsHelper.boto3_sts(arn, role_session_name, external_id)
            client = boto3.client(
                service_name,
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken'],
                region_name=region_name,
                config=Config(retries={'max_attempts': AwsHelper.boto3_retry_config()})
            )
        else:
            client = boto3.client(
                service_name,
                region_name=region_name,
                config=Config(retries={'max_attempts': AwsHelper.boto3_retry_config()})
            )

        return client

    @staticmethod
    def boto3_session(service_name, region_name=None, arn=None, role_session_name=None, external_id=None):
        if arn is not None:
            credentials = AwsHelper.boto3_sts(arn, role_session_name, external_id)
            session = boto3.session.Session(
                region_name=region_name,
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken'],
            ).resource(service_name)
        else:
            session = boto3.session.Session(region_name=region_name).resource(service_name)
        return session

    @staticmethod
    def boto3_designation_credentials(service_name, aws_access_key_id, aws_secret_access_key, account_type):
        """
        A method to initialize an AWS service connection with access/secret access keys.
        :param service_name:
        :param aws_access_key_id:
        :param aws_secret_access_key:
        :param account_type:
        :return: (object) the AWS connection object.
        """
        if account_type:
            region_name = AwsHelper.boto3_china_region()
        else:
            region_name = AwsHelper.boto3_standard_region()

        session = boto3.Session(
            aws_access_key_id='{}'.format(aws_access_key_id),
            aws_secret_access_key='{}'.format(aws_secret_access_key),
            region_name='{}'.format(region_name),
        )
        sts_client = session.client('{}'.format(service_name))
        return sts_client

    @staticmethod
    def boto3_assume_role(sts_client, role_arn, external_id, role_session_name):
        if external_id is not None:
            assumed_role_object = sts_client.assume_role(
                RoleArn=role_arn, ExternalId=external_id,
                RoleSessionName=role_session_name,
            )
        else:
            assumed_role_object = sts_client.assume_role(
                RoleArn=role_arn, RoleSessionName=role_session_name
            )
        return assumed_role_object
