# Generated by Django 2.0.6 on 2018-07-29 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0016_attachment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='size',
        ),
    ]
