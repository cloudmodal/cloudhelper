#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: queue.py
@ide: PyCharm
@time: 2020/3/19 23:20
@desc:
"""
import json
import boto3
import logging
from botocore.exceptions import ClientError
from django.conf import settings
from datetime import datetime

from common.utils import ComplexEncoder

logger = logging.getLogger(__name__)


class InspectQueue:
    wait_period = 0
    queue_url = settings.INSPECT_SQS_QUEUE_URL
    key_id = settings.AWS_ACCESS_KEY_ID
    access_key = settings.AWS_SECRET_ACCESS_KEY
    region = settings.AWS_DEFAULT_REGION

    def __init__(self):
        # Max wait time is 900, if is set to greater, set value to 900
        self.wait_period = int(self.wait_period) if int(self.wait_period) < 900 else 900
        logger.info(f"Initialized sqs service with message delay of {self.wait_period} seconds")
        self.sqs = boto3.client(
            'sqs', aws_access_key_id=self.key_id,
            aws_secret_access_key=self.access_key, region_name=self.region,
        )

    def send(self, message):
        if isinstance(message, dict):
            message['Timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
            message = json.dumps(message, cls=ComplexEncoder)

        if self.queue_url is not None:
            try:
                self.sqs.send_message(
                    QueueUrl=self.queue_url,
                    DelaySeconds=self.wait_period,
                    MessageBody=message
                )
            except ClientError:
                logger.exception(
                    'Failed to send message to sqs queue, The security token included in the request is invalid.'
                )
                logger.error(f"Message:{message}")
