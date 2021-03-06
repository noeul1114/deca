# Generated by Django 2.0.6 on 2018-07-24 16:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0014_vote_up_down'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='article',
        ),
        migrations.AddField(
            model_name='vote',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 24, 16, 5, 39, 686547, tzinfo=utc), verbose_name='Date published'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vote',
            name='ip',
            field=models.GenericIPAddressField(),
        ),
    ]
