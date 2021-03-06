# Generated by Django 2.1.7 on 2019-07-06 22:12

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('galleries', '0011_remove_category_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogHomeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('bedroom', models.IntegerField(default=1)),
                ('bathroom', models.FloatField()),
                ('story', models.FloatField(default=1)),
                ('wide', models.FloatField()),
                ('deep', models.FloatField()),
                ('description', ckeditor.fields.RichTextField(blank=True, default='')),
            ],
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('-date',)},
        ),
        migrations.RemoveField(
            model_name='buildingimages',
            name='category',
        ),
        migrations.RemoveField(
            model_name='category',
            name='level',
        ),
        migrations.RemoveField(
            model_name='category',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='category',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='category',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='category',
            name='tree_id',
        ),
        migrations.AddField(
            model_name='category',
            name='images',
            field=models.ManyToManyField(to='galleries.BuildingImages'),
        ),
        migrations.AddField(
            model_name='category',
            name='location',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='galleries.Location'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='year',
            field=models.IntegerField(default=2000),
        ),
        migrations.AlterField(
            model_name='buildingimages',
            name='title',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=64),
        ),
    ]
