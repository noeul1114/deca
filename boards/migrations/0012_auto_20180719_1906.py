# Generated by Django 2.0.6 on 2018-07-19 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0011_auto_20180711_0256'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='comment_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='shared',
            field=models.IntegerField(default=0),
        ),
    ]
