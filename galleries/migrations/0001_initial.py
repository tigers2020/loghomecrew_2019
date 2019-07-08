# Generated by Django 2.0 on 2017-12-18 16:18

import django.db.models.deletion
import django_resized.forms
from django.db import migrations, models

import galleries.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(allow_unicode=True, editable=False, null=True, unique=True)),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=90, size=[1280, 720], upload_to=galleries.models.image_folder)),
                ('thumb_image', models.ImageField(blank=True, editable=False, upload_to=galleries.models.image_folder)),
                ('description', models.TextField()),
                ('imgorigsize', models.IntegerField(blank=True, editable=False, null=True)),
                ('published', models.BooleanField(default=True)),
                ('date_build', models.DateField(blank=True, editable=False)),
                ('date_build_year', models.CharField(blank=True, max_length=16, null=True)),
            ],
            options={
                'ordering': ['-date_build'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(allow_unicode=True, blank=True, unique=True)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('description', models.TextField(blank=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('published', models.BooleanField(default=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                             to='galleries.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=2)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'ordering': ['-name'],
            },
        ),
        migrations.AddField(
            model_name='buildingimages',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='galleries.Project'),
        ),
        migrations.AddField(
            model_name='buildingimages',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='galleries.Location'),
        ),
    ]
