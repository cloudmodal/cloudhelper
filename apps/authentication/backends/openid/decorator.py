#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: decorator.py
@ide: PyCharm
@time: 2019/12/19 16:35
@desc:
"""
import warnings
import contextlib

import requests
from urllib3.exceptions import InsecureRequestWarning
from django.conf import settings

__all__ = [
    'ssl_verification',
]

old_merge_environment_settings = requests.Session.merge_environment_settings


@contextlib.contextmanager
def no_ssl_verification():
    """
    https://stackoverflow.com/questions/15445981/
    how-do-i-disable-the-security-certificate-check-in-python-requests
    """
    opened_adapters = set()

    def merge_environment_settings(self, url, proxies, stream, verify, cert):
        # Verification happens only once per connection so we need to close
        # all the opened adapters once we're done. Otherwise, the effects of
        # verify=False persist beyond the end of this context manager.
        opened_adapters.add(self.get_adapter(url))
        _settings = old_merge_environment_settings(
            self, url, proxies, stream, verify, cert
        )
        _settings['verify'] = False
        return _settings

    requests.Session.merge_environment_settings = merge_environment_settings
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', InsecureRequestWarning)
            yield
    finally:
        requests.Session.merge_environment_settings = old_merge_environment_settings
        for adapter in opened_adapters:
            try:
                adapter.close()
            except:
                pass


def ssl_verification(func):
    def wrapper(*args, **kwargs):
        if not settings.AUTH_OPENID_IGNORE_SSL_VERIFICATION:
            return func(*args, **kwargs)
        with no_ssl_verification():
            return func(*args, **kwargs)
    return wrapper
