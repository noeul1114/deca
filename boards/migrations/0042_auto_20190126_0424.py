# Generated by Django 2.1.5 on 2019-01-25 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0041_attachment_thumb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='article',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='boards.Article'),
        ),
    ]
