# Generated by Django 2.1.5 on 2019-01-14 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0029_auto_20190114_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionaluserprofile',
            name='nickname',
            field=models.CharField(max_length=30, null=True),
        ),
    ]