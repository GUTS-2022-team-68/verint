# Generated by Django 3.2.12 on 2022-02-12 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0004_auto_20220212_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='score',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employees.score'),
        ),
    ]
