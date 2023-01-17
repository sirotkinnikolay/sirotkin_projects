# Generated by Django 4.1.5 on 2023-01-17 13:04

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_base', '0007_alter_productmodel_create_at'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='productmodel',
            index=django.contrib.postgres.indexes.GinIndex(fields=['products'], name='my_base_pro_product_3948c7_gin'),
        ),
    ]
