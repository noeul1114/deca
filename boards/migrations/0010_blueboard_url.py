# Generated by Django 2.0.6 on 2018-07-10 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0009_auto_20180710_0333'),
    ]

    operations = [
        migrations.AddField(
            model_name='blueboard',
            name='url',
            field=models.CharField(default='blueboard', max_length=50),
            preserve_default=False,
        ),
    ]
