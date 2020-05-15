#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: validators.py
@ide: PyCharm
@time: 2019/12/20 11:21
@desc:
"""
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from rest_framework.validators import (
    UniqueTogetherValidator, ValidationError
)


alphanumeric = RegexValidator(r'^[0-9a-zA-Z_@\-\.]*$', _('Special char not allowed'))


class ProjectUniqueValidator(UniqueTogetherValidator):
    def __call__(self, attrs):
        try:
            super().__call__(attrs)
        except ValidationError as e:
            errors = {}
            for field in self.fields:
                if field == "org_id":
                    continue
                errors[field] = _('This field must be unique.')
            raise ValidationError(errors)
