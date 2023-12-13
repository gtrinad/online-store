# Generated by Django 5.0 on 2023-12-09 20:24

import app_users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAvatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.ImageField(default='avatars/default/default.jpg', upload_to=app_users.models.user_avatar_directory_path, verbose_name='Avatar link')),
                ('alt', models.CharField(default="User's default avatar", max_length=128, verbose_name='Avatar description')),
            ],
            options={
                'verbose_name': 'Avatar',
                'verbose_name_plural': 'Avatars',
            },
        ),
    ]
