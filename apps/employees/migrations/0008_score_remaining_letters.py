# Generated by Django 3.2.12 on 2022-02-12 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0007_auto_20220212_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='remaining_letters',
            field=models.IntegerField(default=5),
        ),
    ]