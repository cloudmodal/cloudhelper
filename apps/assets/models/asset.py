#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: asset.py
@ide: PyCharm
@time: 2020/5/7 11:24
@desc:
"""
import uuid
import logging
from collections import OrderedDict
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .utils import Connectivity
from organization.mixins.models import OrgModelMixin, OrgManager

__all__ = ['Asset', 'ProtocolsMixin']

logger = logging.getLogger(__name__)


class AssetQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def valid(self):
        return self.active()

    def has_protocol(self, name):
        return self.filter(protocols__contains=name)


class ProtocolsMixin:
    protocols = ''
    PROTOCOL_SSH = 'ssh'
    PROTOCOL_RDP = 'rdp'
    PROTOCOL_TELNET = 'telnet'
    PROTOCOL_VNC = 'vnc'
    PROTOCOL_CHOICES = (
        (PROTOCOL_SSH, 'ssh'),
        (PROTOCOL_RDP, 'rdp'),
        (PROTOCOL_TELNET, 'telnet'),
        (PROTOCOL_VNC, 'vnc'),
    )

    @property
    def protocols_as_list(self):
        if not self.protocols:
            return []
        return self.protocols.split(' ')

    @property
    def protocols_as_dict(self):
        d = OrderedDict()
        protocols = self.protocols_as_list
        for i in protocols:
            if '/' not in i:
                continue
            name, port = i.split('/')[:2]
            if not all([name, port]):
                continue
            d[name] = int(port)
        return d

    @property
    def protocols_as_json(self):
        return [
            {"name": name, "port": port}
            for name, port in self.protocols_as_dict.items()
        ]

    def has_protocol(self, name):
        return name in self.protocols_as_dict

    @property
    def ssh_port(self):
        return self.protocols_as_dict.get("ssh", 22)


class Asset(ProtocolsMixin, OrgModelMixin):
    # Important
    PLATFORM_CHOICES = (
        ('Linux', 'Linux'),
        ('Unix', 'Unix'),
        ('MacOS', 'MacOS'),
        ('BSD', 'BSD'),
        ('Windows', 'Windows'),
        ('Windows2012', 'Windows(2012)'),
        ('Windows2016', 'Windows(2016)'),
        ('Windows2019', 'Windows(2019)'),
        ('Other', 'Other'),
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    ip = models.CharField(
        max_length=128, verbose_name=_('IP'), db_index=True
    )
    instance_id = models.CharField(
        blank=True, null=True,
        max_length=128, verbose_name=_('Instance ID')
    )
    instance_type = models.CharField(
        blank=True, null=True,
        max_length=128, verbose_name=_('Instance Type')
    )
    instance_state = models.CharField(
        blank=True, null=True,
        max_length=128, verbose_name=_('Instance State')
    )
    hostname = models.CharField(
        max_length=128, verbose_name=_('Hostname')
    )
    protocol = models.CharField(
        max_length=128, default=ProtocolsMixin.PROTOCOL_SSH,
        choices=ProtocolsMixin.PROTOCOL_CHOICES, verbose_name=_('Protocol')
    )
    platform = models.CharField(
        max_length=128, choices=PLATFORM_CHOICES,
        default='Linux', verbose_name=_('Platform')
    )
    port = models.IntegerField(default=22, verbose_name=_('Port'))
    public_ip = models.CharField(
        blank=True, null=True,
        max_length=128, verbose_name=_('Public IP'), db_index=True
    )
    private_ip = models.CharField(
        blank=True, null=True,
        max_length=128, verbose_name=_('Private IP'), db_index=True
    )
    is_active = models.BooleanField(
        default=True, verbose_name=_('Is active')
    )
    # Auth
    admin_user = models.ForeignKey(
        'assets.AdminUser', on_delete=models.PROTECT, null=True,
        verbose_name=_("Admin user"), related_name='assets'
    )
    sn = models.CharField(
        max_length=128, null=True,
        blank=True, verbose_name=_('Serial number')
    )
    cpu_model = models.CharField(
        max_length=64, null=True, blank=True, verbose_name=_('CPU model')
    )
    cpu_count = models.IntegerField(
        null=True, verbose_name=_('CPU count')
    )
    cpu_cores = models.IntegerField(
        null=True, verbose_name=_('CPU cores')
    )
    cpu_vcpus = models.IntegerField(
        null=True, verbose_name=_('CPU vcpus')
    )
    memory = models.CharField(
        max_length=64, null=True, blank=True, verbose_name=_('Memory')
    )
    disk_total = models.CharField(
        max_length=1024, null=True, blank=True, verbose_name=_('Disk total')
    )
    disk_info = models.CharField(
        max_length=1024, null=True, blank=True, verbose_name=_('Disk info')
    )
    os = models.CharField(
        max_length=128, null=True, blank=True, verbose_name=_('OS')
    )
    os_version = models.CharField(
        max_length=16, null=True, blank=True, verbose_name=_('OS version')
    )
    os_arch = models.CharField(
        max_length=16, blank=True, null=True, verbose_name=_('OS arch')
    )
    hostname_raw = models.CharField(
        max_length=128, blank=True, null=True, verbose_name=_('Hostname raw')
    )
    tags = models.ManyToManyField(
        'assets.Tags', blank=True,
        related_name='assets', verbose_name=_("Tags")
    )
    created_by = models.CharField(
        max_length=32, null=True,
        blank=True, verbose_name=_('Created by')
    )
    date_created = models.DateTimeField(
        auto_now_add=True, null=True,
        blank=True, verbose_name=_('Date created')
    )
    comment = models.TextField(
        max_length=128, default='',
        blank=True, verbose_name=_('Comment')
    )

    objects = OrgManager.from_queryset(AssetQuerySet)()
    _connectivity = None

    def __str__(self):
        return '{0.hostname}({0.ip})'.format(self)

    @property
    def is_valid(self):
        warning = ''
        if not self.is_active:
            warning += ' inactive'
        if warning:
            return False, warning
        return True, warning

    def is_windows(self):
        if self.platform in ("Windows", "Windows2012", "Windows2016", "Windows2019"):
            return True
        else:
            return False

    def is_unix_like(self):
        if self.platform not in ("Windows", "Windows2012", "Windows2016", "Windows2019", "Other"):
            return True
        else:
            return False

    def is_support_ansible(self):
        return self.has_protocol('ssh') and self.platform not in ("Other",)

    @property
    def cpu_info(self):
        info = ""
        if self.cpu_model:
            info += self.cpu_model
        if self.cpu_count and self.cpu_cores:
            info += "{}*{}".format(self.cpu_count, self.cpu_cores)
        return info

    @property
    def hardware_info(self):
        if self.cpu_count:
            return '{} Core {} {}'.format(
                self.cpu_vcpus or self.cpu_count * self.cpu_cores,
                self.memory, self.disk_total
            )
        else:
            return ''

    @property
    def connectivity(self):
        if self._connectivity:
            return self._connectivity
        if not self.admin_user:
            return Connectivity.unknown()
        connectivity = self.admin_user.get_asset_connectivity(self)
        return connectivity

    @connectivity.setter
    def connectivity(self, value):
        if not self.admin_user:
            return
        self.admin_user.set_asset_connectivity(self, value)

    def get_auth_info(self):
        if not self.admin_user:
            return {}

        self.admin_user.load_specific_asset_auth(self)
        info = {
            'username': self.admin_user.username,
            'password': self.admin_user.password,
            'private_key': self.admin_user.private_key_file,
        }
        return info

    class Meta:
        unique_together = [('org_id', 'hostname')]
        verbose_name = _("Asset")
