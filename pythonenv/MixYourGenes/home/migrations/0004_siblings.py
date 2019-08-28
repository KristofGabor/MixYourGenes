# Generated by Django 2.2.4 on 2019-08-28 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20190806_1312'),
    ]

    operations = [
        migrations.CreateModel(
            name='Siblings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sibling', models.ForeignKey(on_delete=False, related_name='Sibling', to='home.UserProfileInfo')),
                ('user', models.ForeignKey(on_delete=False, related_name='User', to='home.UserProfileInfo')),
            ],
        ),
    ]
