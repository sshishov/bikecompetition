# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.PositiveSmallIntegerField(default=0, choices=[(0, 'Pending'), (1, 'Started'), (2, 'Finished')])),
                ('type', models.PositiveSmallIntegerField(default=0, choices=[(0, 'Time Cpmpetition'), (1, 'Distance Cpmpetition')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Competitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompetitorStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('distance', models.PositiveIntegerField()),
                ('competition', models.ForeignKey(to='bc.Competition')),
                ('competitor', models.ForeignKey(to='bc.Competitor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='competition',
            name='competitors',
            field=models.ManyToManyField(to='bc.Competitor'),
            preserve_default=True,
        ),
    ]
