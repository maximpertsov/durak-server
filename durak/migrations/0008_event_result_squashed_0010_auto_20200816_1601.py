# Generated by Django 3.0.8 on 2020-08-17 01:07

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    replaces = [('durak', '0008_event_result'), ('durak', '0009_auto_20200816_1523'), ('durak', '0010_auto_20200816_1601')]

    dependencies = [
        ('durak', '0007_auto_20200804_0257'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='to_state',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]