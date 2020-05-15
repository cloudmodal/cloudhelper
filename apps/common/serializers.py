#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: serializers.py
@ide: PyCharm
@time: 2019/12/20 11:22
@desc:
"""
from rest_framework_bulk.serializers import BulkListSerializer
from rest_framework import serializers
from .mixins import BulkListSerializerMixin


class AdaptedBulkListSerializer(BulkListSerializerMixin, BulkListSerializer):
    pass


class CeleryTaskSerializer(serializers.Serializer):
    task = serializers.CharField(read_only=True)
