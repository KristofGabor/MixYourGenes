# Generated by Django 2.2.4 on 2019-08-28 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20190828_1931'),
        ('GeneTest', '0002_auto_20190805_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='tests',
            name='accessor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Child', to='home.UserProfileInfo'),
        ),
    ]