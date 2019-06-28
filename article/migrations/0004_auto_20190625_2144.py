# Generated by Django 2.1.7 on 2019-06-26 01:44

import django_resized.forms
from django.db import migrations

import article.models


class Migration(migrations.Migration):
    dependencies = [
        ('article', '0003_auto_20171220_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articletext',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True,
                                                         null=True, quality=90, size=[1920, 1080],
                                                         upload_to=article.models.static_folder),
        ),
    ]