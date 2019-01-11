# Generated by Django 2.0.6 on 2018-07-29 13:14

from django.db import migrations, models
import django.db.models.deletion
from django_summernote.utils import get_attachment_upload_to


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0015_auto_20180725_0105'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Defaults to filename, if left blank', max_length=255, null=True)),
                ('file', models.FileField(upload_to=get_attachment_upload_to())),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('size', models.IntegerField(null=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boards.Article')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
