# Generated by Django 2.0.6 on 2018-07-30 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0021_auto_20180730_2321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='user',
        ),
        migrations.AddField(
            model_name='attachment',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='boards.Article'),
        ),
    ]
