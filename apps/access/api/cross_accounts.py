#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: cross_accounts.py
@ide: PyCharm
@time: 2020/2/15 10:39
@desc:
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from common.permissions import IsValidUser
from ..utils import cross_accounts


class CrossAccountsListView(APIView):
    http_method_names = ['get']
    permission_classes = (IsValidUser,)
    object = None

    def get(self, request):
        accounts = cross_accounts(self.request.user.email)

        data = {
            "code": status.HTTP_200_OK,
            "data": accounts,
            "msg": "Account information filled in across accounts"
        }
        return Response(data, status=status.HTTP_200_OK)
