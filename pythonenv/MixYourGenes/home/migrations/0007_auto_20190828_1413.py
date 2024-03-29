# Generated by Django 2.2.4 on 2019-08-28 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_remove_userprofileinfo_portfolio_site'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofileinfo',
            name='dad',
        ),
        migrations.RemoveField(
            model_name='userprofileinfo',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='userprofileinfo',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='userprofileinfo',
            name='mom',
        ),
        migrations.CreateModel(
            name='Parents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dad', models.ForeignKey(default=None, on_delete=False, related_name='DAD', to='home.UserProfileInfo')),
                ('mom', models.ForeignKey(default=None, on_delete=False, related_name='MOM', to='home.UserProfileInfo')),
            ],
        ),
    ]
