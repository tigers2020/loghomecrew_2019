# Generated by Django 2.1.7 on 2019-06-27 00:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('galleries', '0007_auto_20190626_0630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingimages',
            name='date_build',
            field=models.DateTimeField(blank=True, editable=False),
        ),
    ]