# Generated by Django 3.2.12 on 2022-02-12 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_wordoftheday'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordOfTheDayWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('height', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='WordOfTheDay',
        ),
    ]
