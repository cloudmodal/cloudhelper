# Generated by Django 2.2.10 on 2020-05-25 05:06

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=128, verbose_name='Username')),
                ('type', models.CharField(choices=[('W', 'Web'), ('T', 'Terminal')], max_length=2, verbose_name='Login type')),
                ('ip', models.GenericIPAddressField(verbose_name='Login ip')),
                ('city', models.CharField(blank=True, max_length=254, null=True, verbose_name='Login city')),
                ('user_agent', models.CharField(blank=True, max_length=254, null=True, verbose_name='User agent')),
                ('mfa', models.SmallIntegerField(choices=[(0, 'Disabled'), (1, 'Enabled'), (2, '-')], default=2, verbose_name='MFA')),
                ('reason', models.CharField(blank=True, default='', max_length=128, verbose_name='Reason')),
                ('status', models.BooleanField(choices=[(True, 'Success'), (False, 'Failed')], default=True, max_length=2, verbose_name='Status')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date login')),
            ],
            options={
                'ordering': ['-datetime', 'username'],
            },
        ),
        migrations.CreateModel(
            name='OperateLog',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=128, verbose_name='User')),
                ('action', models.CharField(choices=[('create', 'Create'), ('update', 'Update'), ('delete', 'Delete')], max_length=16, verbose_name='Action')),
                ('resource_type', models.CharField(max_length=64, verbose_name='Resource Type')),
                ('resource', models.CharField(max_length=128, verbose_name='Resource')),
                ('remote_addr', models.CharField(blank=True, max_length=15, null=True, verbose_name='Remote addr')),
                ('datetime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PasswordLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=128, verbose_name='User')),
                ('change_by', models.CharField(max_length=128, verbose_name='Change by')),
                ('remote_addr', models.CharField(blank=True, max_length=15, null=True, verbose_name='Remote addr')),
                ('datetime', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
