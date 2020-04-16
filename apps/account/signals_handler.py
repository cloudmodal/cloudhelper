#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: signals_handler.py.py
@ide: PyCharm
@time: 2019/12/19 18:51
@desc:
"""
from django.dispatch import receiver
from common.utils import get_logger
from .signals import post_user_create, post_user_registered


logger = get_logger(__file__)


@receiver(post_user_create)
def on_user_create(sender, user=None, **kwargs):
    logger.debug("接收用户`{}`创建信号".format(user.name))
    from common.send_email import send_user_created_mail
    logger.info("   - 发送欢迎邮件 ...".format(user.name))
    if user.email:
        send_user_created_mail(user)


@receiver(post_user_registered)
def on_user_create(sender, user=None, **kwargs):
    logger.debug("接收用户`{}`创建信号".format(user.name))
    from common.send_email import send_user_registered_mail
    logger.info("   - 发送欢迎邮件 ...".format(user.name))
    if user.email:
        send_user_registered_mail(user)
