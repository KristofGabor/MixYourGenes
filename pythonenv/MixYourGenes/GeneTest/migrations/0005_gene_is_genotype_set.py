# Generated by Django 2.2.4 on 2019-09-02 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GeneTest', '0004_gene_isxlinked'),
    ]

    operations = [
        migrations.AddField(
            model_name='gene',
            name='is_genotype_set',
            field=models.BooleanField(default=False),
        ),
    ]
