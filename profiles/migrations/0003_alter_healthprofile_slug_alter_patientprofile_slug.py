# Generated by Django 4.0.4 on 2022-07-27 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_healthprofile_documenttype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthprofile',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]