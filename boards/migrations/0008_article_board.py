# Generated by Django 2.0.6 on 2018-07-09 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0007_blueboard'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='board',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='boards.BlueBoard'),
            preserve_default=False,
        ),
    ]
