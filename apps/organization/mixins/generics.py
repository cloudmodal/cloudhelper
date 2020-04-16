#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: generics.py
@ide: PyCharm
@time: 2019/12/20 11:32
@desc:
"""
from rest_framework import generics

from .api import OrgQuerySetMixin


class ListAPIView(OrgQuerySetMixin, generics.ListAPIView):
    pass


class RetrieveAPIView(OrgQuerySetMixin, generics.RetrieveAPIView):
    pass


class CreateAPIView(OrgQuerySetMixin, generics.CreateAPIView):
    pass


class DestroyAPIView(OrgQuerySetMixin, generics.DestroyAPIView):
    pass


class ListCreateAPIView(OrgQuerySetMixin, generics.ListCreateAPIView):
    pass


class UpdateAPIView(OrgQuerySetMixin, generics.UpdateAPIView):
    pass


class RetrieveUpdateAPIView(OrgQuerySetMixin, generics.RetrieveUpdateAPIView):
    pass


class RetrieveDestroyAPIView(OrgQuerySetMixin, generics.RetrieveDestroyAPIView):
    pass


class RetrieveUpdateDestroyAPIView(OrgQuerySetMixin, generics.RetrieveUpdateDestroyAPIView):
    pass
