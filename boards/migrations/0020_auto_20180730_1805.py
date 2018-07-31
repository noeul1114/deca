# Generated by Django 2.0.6 on 2018-07-30 09:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boards', '0019_attachment_article'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='article',
        ),
        migrations.RemoveField(
            model_name='attachment',
            name='size',
        ),
        migrations.AddField(
            model_name='attachment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]