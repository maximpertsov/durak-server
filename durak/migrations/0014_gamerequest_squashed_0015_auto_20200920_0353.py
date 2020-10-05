# Generated by Django 3.0.8 on 2020-09-20 20:04

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('durak', '0013_auto_20200909_0124'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameters', django.contrib.postgres.fields.jsonb.JSONField()),
                ('players', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='durak.GameVariant')),
            ],
        ),
    ]