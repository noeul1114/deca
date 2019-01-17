# Generated by Django 2.1.5 on 2019-01-17 18:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import storages.backends.ftp
import tutorialPoll.custom_upload_path


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boards', '0037_board_has_lower_board'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(blank=True, help_text='Defaults to filename, if left blank', max_length=255, null=True)),
                ('file', models.ImageField(storage=storages.backends.ftp.FTPStorage(), upload_to=tutorialPoll.custom_upload_path.custom_uploaded_filepath_debug_board_image)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='additionaluserprofile',
            name='image',
        ),
        migrations.AlterField(
            model_name='additionaluserprofile',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True),
        ),
    ]