# Generated by Django 2.2.16 on 2021-03-12 03:00

import assets.models.asset
import common.fields.model
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.fields
import uuid


def add_default_region(apps, schema_editor):
    region_model = apps.get_model("assets", "Region")
    db_alias = schema_editor.connection.alias
    region_model.objects.using(db_alias).create(
        name="Default", owner="System",
        comment="Default region"
    )


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('access', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('username', models.CharField(blank=True, db_index=True, max_length=32, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z_@\\-\\.]*$', 'Special char not allowed')], verbose_name='Username')),
                ('password', common.fields.model.EncryptCharField(blank=True, max_length=256, null=True, verbose_name='Password')),
                ('private_key', common.fields.model.EncryptTextField(blank=True, null=True, verbose_name='SSH private key')),
                ('public_key', common.fields.model.EncryptTextField(blank=True, null=True, verbose_name='SSH public key')),
                ('comment', models.TextField(blank=True, verbose_name='Comment')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('created_by', models.CharField(max_length=128, null=True, verbose_name='Created by')),
                ('become', models.BooleanField(default=True)),
                ('become_method', models.CharField(choices=[('sudo', 'sudo'), ('su', 'su')], default='sudo', max_length=4)),
                ('become_user', models.CharField(default='root', max_length=64)),
                ('_become_pass', models.CharField(blank=True, default='', max_length=128)),
            ],
            options={
                'verbose_name': 'Admin user',
                'ordering': ['name'],
                'unique_together': {('name', 'org_id')},
            },
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('ip', models.CharField(db_index=True, max_length=128, verbose_name='IP')),
                ('instance_id', models.CharField(blank=True, max_length=128, null=True, verbose_name='Instance ID')),
                ('instance_type', models.CharField(blank=True, max_length=128, null=True, verbose_name='Instance Type')),
                ('instance_state', models.CharField(blank=True, max_length=128, null=True, verbose_name='Instance State')),
                ('hostname', models.CharField(max_length=128, verbose_name='Hostname')),
                ('protocol', models.CharField(choices=[('ssh', 'ssh'), ('rdp', 'rdp'), ('telnet', 'telnet'), ('vnc', 'vnc')], default='ssh', max_length=128, verbose_name='Protocol')),
                ('platform', models.CharField(choices=[('Linux', 'Linux'), ('Unix', 'Unix'), ('MacOS', 'MacOS'), ('BSD', 'BSD'), ('Windows', 'Windows'), ('Windows2012', 'Windows(2012)'), ('Windows2016', 'Windows(2016)'), ('Windows2019', 'Windows(2019)'), ('Other', 'Other')], default='Linux', max_length=128, verbose_name='Platform')),
                ('port', models.IntegerField(default=22, verbose_name='Port')),
                ('public_ip', models.CharField(blank=True, db_index=True, max_length=128, null=True, verbose_name='Public IP')),
                ('private_ip', models.CharField(blank=True, db_index=True, max_length=128, null=True, verbose_name='Private IP')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('sn', models.CharField(blank=True, max_length=128, null=True, verbose_name='Serial number')),
                ('cpu_model', models.CharField(blank=True, max_length=64, null=True, verbose_name='CPU model')),
                ('cpu_count', models.IntegerField(null=True, verbose_name='CPU count')),
                ('cpu_cores', models.IntegerField(null=True, verbose_name='CPU cores')),
                ('cpu_vcpus', models.IntegerField(null=True, verbose_name='CPU vcpus')),
                ('memory', models.CharField(blank=True, max_length=64, null=True, verbose_name='Memory')),
                ('disk_total', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Disk total')),
                ('disk_info', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Disk info')),
                ('os', models.CharField(blank=True, max_length=128, null=True, verbose_name='OS')),
                ('os_version', models.CharField(blank=True, max_length=16, null=True, verbose_name='OS version')),
                ('os_arch', models.CharField(blank=True, max_length=16, null=True, verbose_name='OS arch')),
                ('hostname_raw', models.CharField(blank=True, max_length=128, null=True, verbose_name='Hostname raw')),
                ('created_by', models.CharField(blank=True, max_length=32, null=True, verbose_name='Created by')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('comment', models.TextField(blank=True, default='', max_length=128, verbose_name='Comment')),
                ('admin_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='assets', to='assets.AdminUser', verbose_name='Admin user')),
            ],
            options={
                'verbose_name': 'Asset',
            },
            bases=(assets.models.asset.ProtocolsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CommandFilter',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('comment', models.TextField(blank=True, default='', verbose_name='Comment')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, default='', max_length=128, verbose_name='Created by')),
            ],
            options={
                'verbose_name': 'Command filter',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=128, verbose_name='Key')),
                ('value', models.CharField(max_length=128, verbose_name='Value')),
                ('category', models.CharField(choices=[('system', 'System'), ('user', 'User')], default='user', max_length=128, verbose_name='Category')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
            ],
            options={
                'db_table': 'assets_tags',
                'unique_together': {('key', 'value', 'org_id')},
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='Region name')),
                ('owner', models.CharField(blank=True, max_length=32, null=True, verbose_name='Owner')),
                ('telephone', models.CharField(blank=True, max_length=32, null=True, verbose_name='Telephone')),
                ('address', models.CharField(blank=True, max_length=128, null=True, verbose_name='Address')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('parent', models.ForeignKey(blank=True, help_text='Tips: If you create a top-level zone, leave this field blank.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='assets.Region', verbose_name='Parent')),
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': 'Region',
                'db_table': 'assets_region',
            },
        ),
        migrations.CreateModel(
            name='CommandFilterRule',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('regex', 'Regex'), ('command', 'Command')], default='command', max_length=16, verbose_name='Type')),
                ('priority', models.IntegerField(default=50, help_text='1-100, the higher will be match first', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Priority')),
                ('content', models.TextField(help_text='One line one command', max_length=1024, verbose_name='Content')),
                ('action', models.IntegerField(choices=[(0, 'Deny'), (1, 'Allow')], default=0, verbose_name='Action')),
                ('comment', models.CharField(blank=True, default='', max_length=64, verbose_name='Comment')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, default='', max_length=128, verbose_name='Created by')),
                ('filter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rules', to='assets.CommandFilter', verbose_name='Filter')),
            ],
            options={
                'verbose_name': 'Command filter rule',
                'ordering': ('-priority', 'action'),
            },
        ),
        migrations.CreateModel(
            name='AuthBook',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('username', models.CharField(blank=True, db_index=True, max_length=32, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z_@\\-\\.]*$', 'Special char not allowed')], verbose_name='Username')),
                ('password', common.fields.model.EncryptCharField(blank=True, max_length=256, null=True, verbose_name='Password')),
                ('private_key', common.fields.model.EncryptTextField(blank=True, null=True, verbose_name='SSH private key')),
                ('public_key', common.fields.model.EncryptTextField(blank=True, null=True, verbose_name='SSH public key')),
                ('comment', models.TextField(blank=True, verbose_name='Comment')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('created_by', models.CharField(max_length=128, null=True, verbose_name='Created by')),
                ('is_latest', models.BooleanField(default=False, verbose_name='Latest version')),
                ('version', models.IntegerField(default=1, verbose_name='Version')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset', verbose_name='Asset')),
            ],
            options={
                'verbose_name': 'AuthBook',
            },
        ),
        migrations.CreateModel(
            name='AssetConfigs',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Name')),
                ('account', models.CharField(max_length=128, verbose_name='Cloud Account')),
                ('region', models.CharField(help_text='region：AWS：us-east-1 aliyun：cn-hangzhou', max_length=128, verbose_name='Region')),
                ('state', models.BooleanField(default=False, verbose_name='State')),
                ('comment', models.TextField(blank=True, max_length=128, verbose_name='Comment')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('created_by', models.CharField(max_length=128, null=True, verbose_name='Created by')),
                ('credentials', models.ForeignKey(on_delete=django.db.models.fields.NOT_PROVIDED, related_name='assets_cofig', to='access.StatisticsCredential', verbose_name='Credentials')),
                ('default_admin_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assets.AdminUser', verbose_name='Admin user')),
            ],
            options={
                'verbose_name': 'Asset Config',
                'db_table': 'asset_config',
            },
        ),
        migrations.AddField(
            model_name='asset',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='assets_region', to='assets.Region', verbose_name='Region'),
        ),
        migrations.AddField(
            model_name='asset',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='assets', to='assets.Tags', verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='SystemUser',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('username', models.CharField(blank=True, db_index=True, max_length=32, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z_@\\-\\.]*$', 'Special char not allowed')], verbose_name='Username')),
                ('password', common.fields.model.EncryptCharField(blank=True, max_length=256, null=True, verbose_name='Password')),
                ('private_key', common.fields.model.EncryptTextField(blank=True, null=True, verbose_name='SSH private key')),
                ('public_key', common.fields.model.EncryptTextField(blank=True, null=True, verbose_name='SSH public key')),
                ('comment', models.TextField(blank=True, verbose_name='Comment')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('created_by', models.CharField(max_length=128, null=True, verbose_name='Created by')),
                ('priority', models.IntegerField(default=20, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Priority')),
                ('protocol', models.CharField(choices=[('ssh', 'ssh'), ('rdp', 'rdp'), ('telnet', 'telnet'), ('vnc', 'vnc')], default='ssh', max_length=16, verbose_name='Protocol')),
                ('auto_push', models.BooleanField(default=True, verbose_name='Auto push')),
                ('sudo', models.TextField(default='/bin/whoami', verbose_name='Sudo')),
                ('shell', models.CharField(default='/bin/bash', max_length=64, verbose_name='Shell')),
                ('login_mode', models.CharField(choices=[('auto', 'Automatic login'), ('manual', 'Manually login')], default='auto', max_length=10, verbose_name='Login mode')),
                ('assets', models.ManyToManyField(blank=True, to='assets.Asset', verbose_name='Assets')),
                ('cmd_filters', models.ManyToManyField(blank=True, related_name='system_users', to='assets.CommandFilter', verbose_name='Command filter')),
            ],
            options={
                'verbose_name': 'System user',
                'ordering': ['name'],
                'unique_together': {('name', 'org_id')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='asset',
            unique_together={('org_id', 'hostname')},
        ),
        migrations.RunPython(add_default_region),
    ]
