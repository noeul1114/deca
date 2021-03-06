# Generated by Django 2.0.6 on 2018-07-09 08:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='boards.Article'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='writer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
