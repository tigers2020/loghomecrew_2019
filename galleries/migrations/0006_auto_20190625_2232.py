# Generated by Django 2.1.7 on 2019-06-26 02:32

import sorl.thumbnail.fields
from django.db import migrations

import galleries.models


class Migration(migrations.Migration):
    dependencies = [
        ('galleries', '0005_auto_20180110_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingimages',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to=galleries.models.image_folder),
        ),
    ]
