# Generated by Django 4.0.3 on 2022-04-10 09:09

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0005_rename_coords_hotel_coord_x_hotel_coord_y'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
