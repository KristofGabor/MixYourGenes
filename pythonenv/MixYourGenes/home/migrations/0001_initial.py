# Generated by Django 2.2.4 on 2019-08-05 16:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileInfo',
            fields=[
                ('user', models.OneToOneField(on_delete=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('portfolio_site', models.URLField(blank=True)),
                ('profile_pic', models.ImageField(blank=True, upload_to='profile_pictures')),
                ('first_name', models.CharField(default='', max_length=30)),
                ('last_name', models.CharField(default='', max_length=30)),
                ('sex', models.BooleanField(default=True)),
            ],
        ),
    ]
