#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: realtion.py
@ide: PyCharm
@time: 2019/12/20 11:54
@desc:
"""
from rest_framework import serializers

from ..models import User

__all__ = ['UserUserGroupRelationSerializer']


class UserUserGroupRelationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(read_only=True)
    usergroup_name = serializers.CharField(read_only=True)

    class Meta:
        model = User.groups.through
        fields = ['id', 'user', 'user_name', 'usergroup', 'usergroup_name']
