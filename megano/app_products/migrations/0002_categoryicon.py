# Generated by Django 5.0 on 2023-12-11 14:34

import app_products.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryIcon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.ImageField(upload_to=app_products.models.category_image_directory_path, verbose_name='Category link')),
                ('alt', models.CharField(default='Category icon description', max_length=128, verbose_name='Category icon description')),
                ('category', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='image', to='app_products.category')),
            ],
            options={
                'verbose_name': 'Category icon',
                'verbose_name_plural': 'Category icons',
                'ordering': ['pk'],
            },
        ),
    ]