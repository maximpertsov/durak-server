# Generated by Django 3.0.8 on 2020-08-15 15:07

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('durak', '0007_auto_20200804_0257'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='result',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
            preserve_default=False,
        ),
    ]