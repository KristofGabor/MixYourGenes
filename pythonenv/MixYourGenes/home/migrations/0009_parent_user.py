# Generated by Django 2.2.4 on 2019-08-28 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20190828_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='user',
            field=models.ForeignKey(default=None, on_delete=False, related_name='child', to='home.UserProfileInfo'),
        ),
    ]
