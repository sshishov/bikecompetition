# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='limit',
            field=models.FloatField(default=50.0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='competition',
            name='type',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, 'Time Competition'), (1, 'Distance Competition')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='competitorstats',
            name='distance',
            field=models.FloatField(),
            preserve_default=True,
        ),
    ]
