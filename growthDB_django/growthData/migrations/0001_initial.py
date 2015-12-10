# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-09 20:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Design',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=1000)),
                ('type', models.CharField(choices=[('str', 'str'), ('int', 'int'), ('float', 'float')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='DesignElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('strain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='growthData.Design')),
            ],
        ),
        migrations.CreateModel(
            name='ExperimentalDesign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designElements', models.ManyToManyField(to='growthData.DesignElement')),
                ('strain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='growthData.ExperimentalDesign')),
            ],
        ),
        migrations.CreateModel(
            name='Experimenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Plate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('dataFile', models.FileField(upload_to='uploads/%Y/%m/%d/')),
                ('experimenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='growthData.Experimenter')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=1000)),
                ('dataStarted', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Well',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biologicalReplicate', models.IntegerField(default=0)),
                ('technicalReplicate', models.IntegerField(default=0)),
                ('experimentalDesign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='growthData.ExperimentalDesign')),
                ('plate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='growthData.Plate')),
            ],
        ),
        migrations.AddField(
            model_name='plate',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='growthData.Project'),
        ),
    ]
