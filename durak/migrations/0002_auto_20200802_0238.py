# Generated by Django 3.0.8 on 2020-08-02 02:38

import django.contrib.auth.models
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('durak', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(max_length=128)),
                ('payload', django.contrib.postgres.fields.jsonb.JSONField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_set', to='durak.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='durak.Player')),
            ],
        ),
        migrations.AddIndex(
            model_name='event',
            index=models.Index(fields=['type', 'created_at'], name='durak_event_type_3c1dee_idx'),
        ),
    ]