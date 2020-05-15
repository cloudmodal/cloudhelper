#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: aws.py
@ide: PyCharm
@time: 2020/5/12 18:22
@desc:
"""
import boto3
import logging
import botocore
from datetime import datetime
from botocore.exceptions import NoCredentialsError, ClientError


class AWSConnector:
    def __init__(
            self, verbose=None, access_key=None, secret_key=None,
            region=None, org_id='', created_by='', comment=''
    ):
        self.accessKey = access_key
        self.secretKey = secret_key
        self.region = region
        self.verbosity = verbose or 'INFO'
        self.created_by = created_by
        self.org_id = org_id
        self.comment = comment
        self.logger = self._init_logger()

    def _init_logger(self):
        lov = logging.Logger(__name__)
        lov.setLevel(self.verbosity)
        return lov

    def _init_connection(self, service):
        """
        A method to initialize an AWS service connection with access/secret access keys.
        :param service:
        :return: (object) the AWS connection object.
        """
        try:
            s = boto3.Session(
                aws_access_key_id='{}'.format(self.accessKey),
                aws_secret_access_key='{}'.format(self.secretKey),
                region_name='{}'.format(self.region),
            )
            c = s.client('{}'.format(service))
            return c
        except ClientError as e:
            self.logger.error('Error Connecting with the provided credentials. {}'.format(e))
            return []
        except Exception as e:
            self.logger.exception('General Exception ... {}'.format(e))
            return []

    def get_ec2_info(self):
        """
        A method to suggest the right sizing for AWS EC2 Instances.
        :return: (dictionary) The dictionary result of the logic.
        """
        ec2c = self._init_connection('ec2')
        try:
            response = ec2c.describe_instances()
        except ClientError as e:
            self.logger.error('Failed to describe instances... {}'.format(e))
            return []
        except Exception as e:
            self.logger.exception('General Exception... {}'.format(e))
            return []

        ec2info = []

        for a in range(0, len(response['Reservations'])):
            for b in range(0, len(response['Reservations'][a]['Instances'])):
                base = response['Reservations'][a]['Instances'][b]

                asset_data = {}
                if 'Tags' in base:
                    tags = dict(map(lambda tag: (tag['Key'], tag['Value']), base['Tags']))
                    if tags.get('Name'):
                        asset_data['hostname'] = tags.get('Name')
                    else:
                        asset_data['hostname'] = base.get('InstanceId')
                else:
                    asset_data['hostname'] = base.get('InstanceId')

                asset_data['instance_id'] = base.get('InstanceId', 'Null')
                asset_data['instance_type'] = base.get('InstanceType', 'Null')
                asset_data['instance_state'] = base['State'].get('Name', '')
                asset_data['private_ip'] = base.get('PrivateIpAddress', 'Null')
                asset_data['public_ip'] = base.get('PublicIpAddress', asset_data['private_ip'])
                asset_data['cpu_options'] = base.get('CpuOptions', {})
                asset_data['platform'] = base.get('Platform', 'Null')
                asset_data['tags'] = base.get('Tags', [])
                asset_data['org_id'] = self.org_id
                asset_data['comment'] = self.comment
                ec2info.append(asset_data)

        return ec2info


# x = AWSConnector(
#     access_key='AKIA4FU4JFDXHV2MFMEG',
#     secret_key='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',
#     region='cn-northwest-1',
# )
#
# for r in x.get_ec2_info():
#     print(r)
