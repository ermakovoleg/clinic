# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='ФИО')),
            ],
        ),
        migrations.CreateModel(
            name='Reception',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('patient', models.CharField(max_length=100, verbose_name='Пациент')),
                ('datetime', models.DateTimeField()),
                ('doctor', models.ForeignKey(to='register.Doctor')),
            ],
        ),
    ]
