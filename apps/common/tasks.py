#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: tasks.py
@ide: PyCharm
@time: 2019/12/19 16:16
@desc:
"""
import smtplib
import email.utils
from django.conf import settings
from django.core.mail import send_mail
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from celery import shared_task
from .utils import get_logger


logger = get_logger(__file__)


@shared_task
def send_mail_async(*args, **kwargs):
    """ Using celery to send email async

    You can use it as django send_mail function

    Example:
    send_mail_sync.delay(subject, message, from_mail, recipient_list, fail_silently=False, html_message=None)

    Also you can ignore the from_mail, unlike django send_mail, from_email is not a require args:

    Example:
    send_mail_sync.delay(subject, message, recipient_list, fail_silently=False, html_message=None)
    """
    if len(args) == 3:
        args = list(args)
        args[0] = settings.EMAIL_SUBJECT_PREFIX + args[0]
        email_from = settings.EMAIL_FROM or settings.EMAIL_HOST_USER
        args.insert(2, email_from)
        args = tuple(args)

    try:
        return send_mail(*args, **kwargs)
    except Exception as e:
        logger.error("Sending mail error: {}".format(e))


@shared_task
def send_ses_email(**kwargs):
    # 创建消息容器-正确的MIME类型是 multipart/alternative。
    msg = MIMEMultipart('alternative')
    msg['Subject'] = kwargs['SUBJECT']
    msg['From'] = email.utils.formataddr((settings.SES_EMAIL_SENDERNAME, settings.SES_EMAIL_SENDER))
    msg['To'] = kwargs['RECIPIENT']

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(kwargs['BODY_TEXT'], 'plain')
    part2 = MIMEText(kwargs['BODY_HTML'], 'html')
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Try to send the message.
    try:
        server = smtplib.SMTP(settings.SES_EMAIL_HOST, settings.SES_EMAIL_PORT)
        server.ehlo()
        server.starttls()
        # stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(settings.SES_EMAIL_USERNAME_SMTP, settings.SES_EMAIL_PASSWORD_SMTP)
        server.sendmail(settings.SES_EMAIL_SENDER, kwargs['RECIPIENT'], msg.as_string())
        server.close()
    # Display an error message if something goes wrong.
    except Exception as e:
        logger.error("Sending mail error: {}".format(e))
    else:
        return logger.debug('邮件已发送！')
