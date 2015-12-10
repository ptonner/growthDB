# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-10 02:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('growthData', '0003_auto_20151210_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='well',
            name='biologicalReplicate',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='well',
            name='experimentalDesign',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='growthData.ExperimentalDesign'),
        ),
        migrations.AlterField(
            model_name='well',
            name='technicalReplicate',
            field=models.IntegerField(default=0),
        ),
    ]