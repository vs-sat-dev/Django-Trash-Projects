# Generated by Django 4.0.3 on 2022-04-08 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0002_facilities_region_state_hotel_coords_hotel_house_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='describe',
            field=models.TextField(default=None, max_length=4096),
            preserve_default=False,
        ),
    ]
