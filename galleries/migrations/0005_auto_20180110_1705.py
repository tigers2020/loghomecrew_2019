# Generated by Django 2.0 on 2018-01-10 22:05

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galleries', '0004_auto_20171220_1221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buildingimages',
            name='slug',
        ),
        migrations.AlterField(
            model_name='buildingimages',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='buildingimages',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]