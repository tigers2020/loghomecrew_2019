# Generated by Django 2.0 on 2017-12-20 17:21

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('galleries', '0003_auto_20171218_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingimages',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]
