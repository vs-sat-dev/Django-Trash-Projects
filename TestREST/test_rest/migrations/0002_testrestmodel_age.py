# Generated by Django 4.0.4 on 2022-04-20 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_rest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testrestmodel',
            name='age',
            field=models.IntegerField(default=18),
        ),
    ]
