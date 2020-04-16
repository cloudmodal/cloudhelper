#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: manager.py
@ide: PyCharm
@time: 2020/4/9 16:23
@desc:
"""
from django.contrib.auth.models import UserManager

__all__ = 'UsersManager'


class UsersManager(UserManager):
    def create_org_user(self, company, name, email, phone, password, comment='', **extra_fields):
        from organization.models import Organization
        org = Organization.objects.create(name=company, comment=comment)
        user = self.model(
            username=email, name=name, email=email, phone=phone,
            is_active=False, role='User', comment=comment,
            is_first_login=True, created_by=name, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        org.admins.add(user)
        org.users.add(user)
        return user
