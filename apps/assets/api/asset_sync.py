#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: asset_sync.py
@ide: PyCharm
@time: 2020/5/14 23:31
@desc:
"""
from django.http import Http404
from datetime import datetime
from rest_framework.views import APIView
from common.permissions import IsOrgAdmin
from rest_framework.response import Response
from django.utils.translation import ugettext as _
from rest_framework.permissions import AllowAny

from common.utils import get_logger
from assets.models import AssetConfigs
from .. import tasks


logger = get_logger(__file__)
__all__ = [
    'AssetSynchronizeApi'
]


class AssetSynchronizeApi(APIView):
    now = datetime.now()
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        config_id = kwargs.get('pk')

        try:
            config = AssetConfigs.objects.filter(pk=config_id)
        except AssetConfigs.DoesNotExist:
            raise Http404
        res = tasks.assets_sync.delay(config)
        logger.debug(f"AssetConfig {res} on {self.now} to manually synchronize")
        return Response({"msg": _("Assets are syncing")}, status=200)
