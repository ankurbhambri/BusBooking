# Generated by Django 3.0.7 on 2020-07-03 06:32

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='attrs',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
    ]
