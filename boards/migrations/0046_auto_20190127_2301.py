# Generated by Django 2.1.5 on 2019-01-27 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0045_auto_20190126_0441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='boards.Article'),
        ),
    ]
