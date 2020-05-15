#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: const.py
@ide: PyCharm
@time: 2019/12/19 16:08
@desc:
"""
from django.utils.translation import ugettext_lazy as _


create_success_msg = _("%(name)s was created successfully")
update_success_msg = _("%(name)s was updated successfully")

create_success_message = _("%(credentials_name)s was created successfully")
update_success_message = _("%(credentials_name)s was updated successfully")
FILE_END_GUARD = ">>> Content End <<<"
celery_task_pre_key = "CELERY_"
KEY_CACHE_RESOURCES_ID = "RESOURCES_ID_{}"

# AD User AccountDisable
# https://blog.csdn.net/bytxl/article/details/17763975
LDAP_AD_ACCOUNT_DISABLE = 2

GENERAL_FORBIDDEN_SPECIAL_CHARACTERS_HELP_TEXT = _(
    'Cannot contain special characters: [ {} ]'
).format(" ".join(['/', '\\']))

GENERAL_FORBIDDEN_SPECIAL_CHARACTERS_PATTERN = r"[/\\]"

GENERAL_FORBIDDEN_SPECIAL_CHARACTERS_ERROR_MSG = _("* The contains characters that are not allowed")
