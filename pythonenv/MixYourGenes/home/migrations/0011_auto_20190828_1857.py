# Generated by Django 2.2.4 on 2019-08-28 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20190828_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofileinfo',
            name='mom',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='DAD', to='home.UserProfileInfo'),
        ),
        migrations.DeleteModel(
            name='Parent',
        ),
    ]