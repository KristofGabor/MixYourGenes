# Generated by Django 2.2.4 on 2019-08-06 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='sex',
            field=models.BooleanField(choices=[(1, 'Male'), (0, 'Female')], default=True),
        ),
    ]
