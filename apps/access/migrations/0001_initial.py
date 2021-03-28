# Generated by Django 2.2.16 on 2021-03-11 06:27

import common.fields.model
from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import rest_framework.utils.encoders
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StatisticsCredential',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Name')),
                ('credential', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Credentials')),
                ('credentials_name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Credentials Name')),
                ('account_type', models.CharField(blank=True, max_length=50, null=True, verbose_name='Account Type')),
                ('credential_type', models.CharField(blank=True, max_length=128, null=True, verbose_name='Credentials Type')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('created_by', models.CharField(max_length=128, null=True, verbose_name='Created by')),
            ],
            options={
                'verbose_name': 'Credential Statistics',
                'db_table': 'access_statistics_credentials',
            },
        ),
        migrations.CreateModel(
            name='GoogleCredential',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('credentials_name', models.CharField(max_length=256, verbose_name='Credentials Name')),
                ('account_type', models.CharField(max_length=50, verbose_name='Account Type')),
                ('credential_type', models.CharField(max_length=128, verbose_name='Credentials Type')),
                ('comment', models.TextField(blank=True, max_length=128, verbose_name='Comment')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('created_by', models.CharField(max_length=128, null=True, verbose_name='Created by')),
                ('google_service_account_key_json', django.contrib.postgres.fields.jsonb.JSONField(db_index=True, encoder=rest_framework.utils.encoders.JSONEncoder, verbose_name='Google Service Account Key JSON')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_google_credential', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Google Credential',
                'db_table': 'access_google_account_key',
                'ordering': ['credentials_name'],
            },
        ),
        migrations.CreateModel(
            name='AmazonCredentialRole',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('credentials_name', models.CharField(max_length=256, verbose_name='Credentials Name')),
                ('account_type', models.CharField(max_length=50, verbose_name='Account Type')),
                ('credential_type', models.CharField(max_length=128, verbose_name='Credentials Type')),
                ('comment', models.TextField(blank=True, max_length=128, verbose_name='Comment')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('created_by', models.CharField(max_length=128, null=True, verbose_name='Created by')),
                ('role_arn', common.fields.model.EncryptCharField(max_length=256, verbose_name='Amazon Credential Role Arn')),
                ('external_id', models.CharField(blank=True, max_length=128, null=True, verbose_name='External ID')),
                ('require_mfa', models.BooleanField(blank=True, default=False, verbose_name='Require MFA')),
                ('is_local_role', models.BooleanField(blank=True, default=False, help_text="For how to configure local roles, please refer to the <a href='https://docs.aws.amazon.com/cli/?id=docs_gateway' target='_blank'>AWS CLI</a> configuration and introduction", verbose_name='Choose local roles')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_aws_credential_role', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Amazon Credential Role',
                'db_table': 'access_amazon_iam_role',
                'ordering': ['role_arn'],
            },
        ),
        migrations.CreateModel(
            name='AccessKeys',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('credentials_name', models.CharField(max_length=256, verbose_name='Credentials Name')),
                ('account_type', models.CharField(max_length=50, verbose_name='Account Type')),
                ('credential_type', models.CharField(max_length=128, verbose_name='Credentials Type')),
                ('comment', models.TextField(blank=True, max_length=128, verbose_name='Comment')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('created_by', models.CharField(max_length=128, null=True, verbose_name='Created by')),
                ('access_key_id', common.fields.model.EncryptCharField(max_length=256, verbose_name='Access Key ID')),
                ('secret_access_key', common.fields.model.EncryptCharField(max_length=256, verbose_name='Secret Access Key')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_aws_credential', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Credential',
                'db_table': 'access_keys',
                'ordering': ['access_key_id'],
            },
        ),
    ]