#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: __init__.py
@ide: PyCharm
@time: 2020/2/21 21:53
@desc:
"""
import os
from celery import Celery
from kombu import Exchange, Queue
from iam import settings

# 为"celery"程序设置默认的Django模块。
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iam.settings')


app = Celery('iam')

configs = {k: v for k, v in settings.__dict__.items() if k.startswith('CELERY')}
# Using a string here means the worker will not have to
# pickle the object when using Windows.
# app.config_from_object('django.conf:settings', namespace='CELERY')
configs["CELERY_QUEUES"] = [
    Queue("celery", Exchange("celery"), routing_key="celery"),
]
# configs["CELERY_ROUTES"] = {
#     "ops.tasks.run_ansible_task": {'exchange': 'ansible', 'routing_key': 'ansible'},
# }

app.namespace = 'CELERY'
app.conf.update(configs)
app.autodiscover_tasks(lambda: [app_config.split('.')[0] for app_config in settings.INSTALLED_APPS])
